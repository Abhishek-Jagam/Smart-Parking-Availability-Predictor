"""
Generates verified figures and summary tables for Section 4: Data Cleaning and Preprocessing.
1. Target class distribution across chronological splits (Table + Bar plot).
2. Missing values and sensor telemetry anomalies before vs after cleaning (Table).
3. Outlier and boundary handling (Occupancy > Capacity and negative values).
4. Feature scaling and encoding summary table.
5. Train/Val/Test chronological split sizes and date spans table.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.report_style import set_report_style

def generate_section4_artifacts():
    set_report_style()
    
    raw_path = os.path.join(BASE_DIR, "data", "raw", "dataset.csv")
    train_path = os.path.join(BASE_DIR, "data", "processed", "train.csv")
    val_path = os.path.join(BASE_DIR, "data", "processed", "val.csv")
    test_path = os.path.join(BASE_DIR, "data", "processed", "test.csv")
    
    fig_dir = os.path.join(BASE_DIR, "report", "figures")
    tab_dir = os.path.join(BASE_DIR, "report", "tables")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)
    
    # 1. Load Datasets
    raw_df = pd.read_csv(raw_path)
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)
    
    # ---------------------------------------------------------
    # 2. Table: Split Specifications & Date Spans
    # ---------------------------------------------------------
    split_info = [
        {
            "Split": "Training",
            "Samples": len(train_df),
            "Proportion (%)": f"{(len(train_df) / (len(train_df)+len(val_df)+len(test_df)))*100:.1f}%",
            "Start Date": train_df["LastUpdated"].min().split()[0],
            "End Date": train_df["LastUpdated"].max().split()[0],
            "Operating Days": pd.to_datetime(train_df["LastUpdated"]).dt.date.nunique()
        },
        {
            "Split": "Validation",
            "Samples": len(val_df),
            "Proportion (%)": f"{(len(val_df) / (len(train_df)+len(val_df)+len(test_df)))*100:.1f}%",
            "Start Date": val_df["LastUpdated"].min().split()[0],
            "End Date": val_df["LastUpdated"].max().split()[0],
            "Operating Days": pd.to_datetime(val_df["LastUpdated"]).dt.date.nunique()
        },
        {
            "Split": "Held-Out Test",
            "Samples": len(test_df),
            "Proportion (%)": f"{(len(test_df) / (len(train_df)+len(val_df)+len(test_df)))*100:.1f}%",
            "Start Date": test_df["LastUpdated"].min().split()[0],
            "End Date": test_df["LastUpdated"].max().split()[0],
            "Operating Days": pd.to_datetime(test_df["LastUpdated"]).dt.date.nunique()
        },
        {
            "Split": "Total Cleaned",
            "Samples": len(train_df) + len(val_df) + len(test_df),
            "Proportion (%)": "100.0%",
            "Start Date": train_df["LastUpdated"].min().split()[0],
            "End Date": test_df["LastUpdated"].max().split()[0],
            "Operating Days": (
                pd.to_datetime(train_df["LastUpdated"]).dt.date.nunique() +
                pd.to_datetime(val_df["LastUpdated"]).dt.date.nunique() +
                pd.to_datetime(test_df["LastUpdated"]).dt.date.nunique()
            )
        }
    ]
    pd.DataFrame(split_info).to_csv(os.path.join(tab_dir, "dataset_splits.csv"), index=False)
    
    # ---------------------------------------------------------
    # 3. Table: Cleaning & Anomaly Correction Before vs After
    # ---------------------------------------------------------
    raw_neg = int((raw_df["Occupancy"] < 0).sum())
    raw_overflow = int((raw_df["Occupancy"] > raw_df["Capacity"]).sum())
    raw_dups = int(raw_df.duplicated(subset=["SystemCodeNumber", "LastUpdated"]).sum())
    raw_missing = int(raw_df.isna().sum().sum())
    
    # In processed train+val+test:
    all_proc = pd.concat([train_df, val_df, test_df], axis=0)
    proc_neg = int((all_proc["Occupancy"] < 0).sum())
    proc_overflow = int((all_proc["Occupancy"] > all_proc["Capacity"]).sum())
    proc_dups = int(all_proc.duplicated(subset=["SystemCodeNumber", "LastUpdated"]).sum())
    proc_missing = int(all_proc[["Capacity", "Occupancy", "occupancy_pct", "lag_1", "lag_2", "lag_3"]].isna().sum().sum())
    
    cleaning_table = [
        {"Anomaly / Issue": "Negative Occupancy Readings (< 0)", "Raw Dataset Count": raw_neg, "Processed Dataset Count": proc_neg, "Mitigation Action Applied": "Clipped to 0 bays (sensor underflow artifact)"},
        {"Anomaly / Issue": "Overflow Occupancy (> Capacity)", "Raw Dataset Count": raw_overflow, "Processed Dataset Count": proc_overflow, "Mitigation Action Applied": "Clipped to rated facility capacity"},
        {"Anomaly / Issue": "Duplicate Timestamp Logs", "Raw Dataset Count": raw_dups, "Processed Dataset Count": proc_dups, "Mitigation Action Applied": "Deduplicated, retaining first valid sensor log"},
        {"Anomaly / Issue": "Missing / Null Feature Values", "Raw Dataset Count": raw_missing, "Processed Dataset Count": proc_missing, "Mitigation Action Applied": "Forward/backward chronological fill per car park"}
    ]
    pd.DataFrame(cleaning_table).to_csv(os.path.join(tab_dir, "data_cleaning_audit.csv"), index=False)
    
    # ---------------------------------------------------------
    # 4. Table: Feature Scaling & Encoding Registry
    # ---------------------------------------------------------
    features_registry = [
        {"Feature Name": "Capacity", "Type": "Numeric (Discrete)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Total bays in facility (220 to 4,675 bays)"},
        {"Feature Name": "occupancy_pct", "Type": "Numeric (Continuous)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Current occupancy level (0.0% to 100.0%)"},
        {"Feature Name": "hour", "Type": "Temporal (Integer)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Hour of day (7 to 16)"},
        {"Feature Name": "minute", "Type": "Temporal (Integer)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Minute of sensor update (0 to 59)"},
        {"Feature Name": "dayofweek", "Type": "Temporal (Integer)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Day of week index (0=Monday, 6=Sunday)"},
        {"Feature Name": "is_weekend", "Type": "Binary Indicator", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "1 if Saturday/Sunday, else 0"},
        {"Feature Name": "weekofyear", "Type": "Temporal (Integer)", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Calendar week index (40 to 51)"},
        {"Feature Name": "hour_sin", "Type": "Cyclical Continuous", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "sin(2 * pi * t / 24) diurnal cycle projection"},
        {"Feature Name": "hour_cos", "Type": "Cyclical Continuous", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "cos(2 * pi * t / 24) diurnal cycle projection"},
        {"Feature Name": "SystemCodeNumber_enc", "Type": "Categorical Identifier", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "LabelEncoded car park ID (0 to 29)"},
        {"Feature Name": "lag_1", "Type": "Autoregressive Lag", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Occupancy % ~30 mins prior (t-1)"},
        {"Feature Name": "lag_2", "Type": "Autoregressive Lag", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Occupancy % ~60 mins prior (t-2)"},
        {"Feature Name": "lag_3", "Type": "Autoregressive Lag", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Occupancy % ~90 mins prior (t-3)"},
        {"Feature Name": "rolling_mean_3", "Type": "Rolling Aggregation", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Mean occupancy % over prior 3 time steps"},
        {"Feature Name": "rolling_std_3", "Type": "Rolling Aggregation", "Encoding / Scaling": "StandardScaler (fit on Train)", "Description": "Standard deviation over prior 3 time steps"}
    ]
    pd.DataFrame(features_registry).to_csv(os.path.join(tab_dir, "feature_engineering_registry.csv"), index=False)
    
    # ---------------------------------------------------------
    # 5. Figure: Class Distribution Before and After Balancing
    # ---------------------------------------------------------
    classes = ["Available", "Nearly Full", "Full"]
    tr_counts = train_df["target_class"].value_counts()[classes].values
    val_counts = val_df["target_class"].value_counts()[classes].values
    te_counts = test_df["target_class"].value_counts()[classes].values
    
    tr_pcts = (tr_counts / len(train_df)) * 100.0
    val_pcts = (val_counts / len(val_df)) * 100.0
    te_pcts = (te_counts / len(test_df)) * 100.0
    
    # Class weights applied in Random Forest: n_samples / (n_classes * np.bincount(y))
    class_weights = len(train_df) / (3.0 * tr_counts)
    
    dist_df = pd.DataFrame({
        "Class": classes,
        "Train Count": tr_counts,
        "Train %": [f"{p:.1f}%" for p in tr_pcts],
        "Val %": [f"{p:.1f}%" for p in val_pcts],
        "Test %": [f"{p:.1f}%" for p in te_pcts],
        "Balanced Class Weight": [f"{w:.3f}" for w in class_weights]
    })
    dist_df.to_csv(os.path.join(tab_dir, "class_distribution_summary.csv"), index=False)
    
    # Plot Class Distribution across Splits
    x = np.arange(len(classes))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.bar(x - width, tr_pcts, width, label="Train Split (70%)", color="#0ea5e9", edgecolor="#0284c7")
    ax.bar(x, val_pcts, width, label="Validation Split (15%)", color="#0f172a", edgecolor="#020617")
    ax.bar(x + width, te_pcts, width, label="Held-Out Test Split (15%)", color="#64748b", edgecolor="#475569")
    
    ax.set_ylabel("Proportion of Observations (%)")
    ax.set_xlabel("Target Availability Category")
    ax.set_xticks(x)
    ax.set_xticklabels(["Available (<50%)", "Nearly Full (50–79%)", "Full (≥80%)"])
    ax.set_ylim(0, 65)
    ax.legend(frameon=True, loc="upper right")
    
    # Add data labels
    for i in range(len(classes)):
        ax.text(x[i] - width, tr_pcts[i] + 1.0, f"{tr_pcts[i]:.1f}%", ha="center", fontsize=8.5)
        ax.text(x[i], val_pcts[i] + 1.0, f"{val_pcts[i]:.1f}%", ha="center", fontsize=8.5)
        ax.text(x[i] + width, te_pcts[i] + 1.0, f"{te_pcts[i]:.1f}%", ha="center", fontsize=8.5)
        
    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "target_class_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    # ---------------------------------------------------------
    # 6. Figure: Sensor Outlier & Clipping Boundary Plot
    # ---------------------------------------------------------
    raw_occ_pct = (raw_df["Occupancy"] / raw_df["Capacity"]) * 100.0
    clean_occ_pct = (all_proc["Occupancy"] / all_proc["Capacity"]) * 100.0
    
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    sns.kdeplot(raw_occ_pct, ax=ax, label="Raw Sensor Readings (Unbounded)", color="#e11d48", linewidth=1.8, linestyle="--")
    sns.kdeplot(clean_occ_pct, ax=ax, label="Cleaned Telemetry (Bounded [0%, 100%])", color="#059669", linewidth=2.0)
    
    ax.axvline(0, color="#94a3b8", linestyle=":", linewidth=1.0)
    ax.axvline(100, color="#94a3b8", linestyle=":", linewidth=1.0)
    ax.axvline(50, color="#d97706", linestyle="-.", linewidth=1.0, label="Availability Thresholds (50% / 80%)")
    ax.axvline(80, color="#d97706", linestyle="-.", linewidth=1.0)
    
    ax.set_xlabel("Facility Occupancy Percentage (%)")
    ax.set_ylabel("Probability Density")
    ax.set_xlim(-15, 120)
    ax.legend(frameon=True, loc="upper right", fontsize=8.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "sensor_boundary_cleaning.png"), dpi=300)
    plt.close()

    print("Section 4 data artifacts generated successfully.")

if __name__ == "__main__":
    generate_section4_artifacts()

