"""
Preprocessing & Leak-Free Feature Engineering Pipeline.
Tailored for UCI Parking Birmingham dataset:
- SystemCodeNumber, Capacity, Occupancy, LastUpdated
- Cleans missing values, negative occupancies, and overflow readings.
- Engineers past-only temporal, lag, and rolling features per car park.
- Performs leakage-free chronological splitting (70% train, 15% val, 15% test).
"""

import os
import sys
import numpy as np
import pandas as pd


FEATURE_COLS = [
    "Capacity",
    "occupancy_pct",
    "hour",
    "minute",
    "dayofweek",
    "is_weekend",
    "weekofyear",
    "hour_sin",
    "hour_cos",
    "SystemCodeNumber_enc",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "rolling_std_3"
]

TARGET_COL = "target_class"
CLASS_NAMES = ["Available", "Nearly Full", "Full"]


def to_availability_class(pct: float) -> str:
    """
    3-Class municipal availability threshold:
    - Available: [0%, 50%)
    - Nearly Full: [50%, 80%)
    - Full: [80%, 100%]
    """
    if pct < 50.0:
        return "Available"
    elif pct < 80.0:
        return "Nearly Full"
    else:
        return "Full"


def load_and_clean_data(file_path: str = "data/raw/dataset.csv") -> pd.DataFrame:
    """
    Loads the Birmingham dataset, handles timestamps, filters/clips anomalies.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw dataset not found at {file_path}")
        
    df = pd.read_csv(file_path)
    print(f"Loaded raw dataset from {file_path} with {len(df):,} records.")
    
    # 1. Parse timestamps
    df["LastUpdated"] = pd.to_datetime(df["LastUpdated"])
    
    # 2. Drop duplicates on SystemCodeNumber and LastUpdated
    initial_len = len(df)
    df = df.drop_duplicates(subset=["SystemCodeNumber", "LastUpdated"]).copy()
    print(f"Removed {initial_len - len(df)} duplicate readings.")
    
    # 3. Sort strictly by car park and timestamp
    df = df.sort_values(by=["SystemCodeNumber", "LastUpdated"]).reset_index(drop=True)
    
    # 4. Clean impossible values
    # Filter non-positive capacities
    df = df[df["Capacity"] > 0].copy()
    
    # Clip negative occupancies to 0
    df["Occupancy"] = df["Occupancy"].clip(lower=0)
    
    # Clip occupancies exceeding physical capacity
    df["Occupancy"] = np.minimum(df["Occupancy"], df["Capacity"])
    
    # Compute current occupancy percentage
    df["occupancy_pct"] = (df["Occupancy"] / df["Capacity"]) * 100.0
    
    # Operating hours filter: Birmingham readings are daytime (07:00 to 17:00)
    df = df[(df["LastUpdated"].dt.hour >= 7) & (df["LastUpdated"].dt.hour <= 17)].copy()
    
    print(f"Cleaned dataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns.")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates temporal, lag, rolling, and target variables without lookahead leakage.
    """
    df = df.copy()
    
    # Temporal attributes
    df["hour"] = df["LastUpdated"].dt.hour
    df["minute"] = df["LastUpdated"].dt.minute
    df["dayofweek"] = df["LastUpdated"].dt.day_of_week
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)
    df["weekofyear"] = df["LastUpdated"].dt.isocalendar().week.astype(int)
    
    # Cyclical hour encoding
    time_decimal = df["hour"] + df["minute"] / 60.0
    df["hour_sin"] = np.sin(time_decimal / 24.0 * 2 * np.pi)
    df["hour_cos"] = np.cos(time_decimal / 24.0 * 2 * np.pi)
    
    # Numerical car park ID encoding (reproducible sorting)
    unique_carparks = sorted(df["SystemCodeNumber"].unique())
    carpark_map = {name: idx for idx, name in enumerate(unique_carparks)}
    df["SystemCodeNumber_enc"] = df["SystemCodeNumber"].map(carpark_map)
    
    # Autoregressive lag features per car park (computed strictly from past)
    df["lag_1"] = df.groupby("SystemCodeNumber")["occupancy_pct"].shift(1)
    df["lag_2"] = df.groupby("SystemCodeNumber")["occupancy_pct"].shift(2)
    df["lag_3"] = df.groupby("SystemCodeNumber")["occupancy_pct"].shift(3)
    
    # Rolling window statistics (past only: shift(1) ensures no current leakage)
    df["rolling_mean_3"] = df.groupby("SystemCodeNumber")["occupancy_pct"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    df["rolling_std_3"] = df.groupby("SystemCodeNumber")["occupancy_pct"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).std()
    ).fillna(0.0)
    
    # Target variable: 1-step ahead occupancy (~30 min future reading)
    df["target_occupancy_pct"] = df.groupby("SystemCodeNumber")["occupancy_pct"].shift(-1)
    
    # Drop rows with NaN from lags or future target
    df = df.dropna(subset=["lag_1", "lag_2", "lag_3", "target_occupancy_pct"]).copy()
    
    # Assign target class
    df["target_class"] = df["target_occupancy_pct"].apply(to_availability_class)
    
    # Persistence Baseline Prediction (predict current occupancy class as future class)
    df["baseline_pred_class"] = df["occupancy_pct"].apply(to_availability_class)
    
    print(f"Features engineered. Final usable dataset: {len(df):,} records.")
    return df


def split_chronologically(df: pd.DataFrame, train_ratio: float = 0.70, val_ratio: float = 0.15):
    """
    Strict chronological split across time to guarantee zero future leakage.
    Train: Earlier 70%, Val: Middle 15%, Test: Later 15%
    """
    df_sorted = df.sort_values(by="LastUpdated").reset_index(drop=True)
    n = len(df_sorted)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train_df = df_sorted.iloc[:train_end].copy()
    val_df = df_sorted.iloc[train_end:val_end].copy()
    test_df = df_sorted.iloc[val_end:].copy()
    
    print(f"\nChronological split summary:")
    print(f"  Train: {len(train_df):,} rows ({train_df['LastUpdated'].min()} to {train_df['LastUpdated'].max()})")
    print(f"  Val:   {len(val_df):,} rows ({val_df['LastUpdated'].min()} to {val_df['LastUpdated'].max()})")
    print(f"  Test:  {len(test_df):,} rows ({test_df['LastUpdated'].min()} to {test_df['LastUpdated'].max()})")
    
    return train_df, val_df, test_df


def save_processed_splits(train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame, output_dir: str = "data/processed"):
    """Saves splits to CSV format."""
    os.makedirs(output_dir, exist_ok=True)
    train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    val_df.to_csv(os.path.join(output_dir, "val.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    print(f"Processed splits saved to {output_dir}/")


def main():
    raw_path = os.path.join("data", "raw", "dataset.csv")
    df_clean = load_and_clean_data(raw_path)
    df_feat = engineer_features(df_clean)
    train_df, val_df, test_df = split_chronologically(df_feat)
    save_processed_splits(train_df, val_df, test_df)


if __name__ == "__main__":
    main()
