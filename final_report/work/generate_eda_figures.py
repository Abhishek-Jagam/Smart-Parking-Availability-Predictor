"""
Generates EDA figures for Section 4:
1. fig_eda_hourly.png (Occupancy by hour)
2. fig_eda_weekday.png (Occupancy by day of week)
3. fig_cleaning_boundary.png (Cleaning illustration: raw unbounded vs clipped)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(BASE_DIR, "final_report", "work")
FIG_DIR = os.path.join(WORK_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# 300 DPI styling
plt.rcParams.clear()
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9.5,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05
})

raw_df = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "dataset.csv"))
train_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "train.csv"))
val_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "val.csv"))
test_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "test.csv"))
all_clean = pd.concat([train_df, val_df, test_df], axis=0)

# 1. Hourly Occupancy Profile
hourly = all_clean.groupby("hour")["occupancy_pct"].agg(["mean", "std"]).reset_index()
fig, ax = plt.subplots(figsize=(6.2, 3.8))
ax.plot(hourly["hour"], hourly["mean"], marker="o", color="#0ea5e9", lw=2.2, label="Mean Occupancy (%)")
ax.fill_between(hourly["hour"], hourly["mean"] - hourly["std"], hourly["mean"] + hourly["std"], color="#0ea5e9", alpha=0.18, label="±1 Std Dev")
ax.axhline(50, color="#d97706", linestyle="--", lw=1.2, label="Nearly Full Threshold (50%)")
ax.set_xlabel("Hour of Day (24-hour format)")
ax.set_ylabel("Occupancy Level (%)")
ax.set_xticks(hourly["hour"])
ax.set_ylim(0, 85)
ax.legend(frameon=True, loc="upper left", fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_eda_hourly.png"), dpi=300)
plt.close()

# 2. Weekday Occupancy Profile
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
all_clean["dow_name"] = all_clean["dayofweek"].map(dow_map)
dow_summary = all_clean.groupby("dow_name")["occupancy_pct"].mean().reindex(dow_order)

fig, ax = plt.subplots(figsize=(6.2, 3.8))
bars = ax.bar(dow_order, dow_summary.values, color="#0f172a", edgecolor="#020617", width=0.55)
ax.axhline(50, color="#d97706", linestyle="--", lw=1.2, label="Nearly Full Threshold (50%)")
ax.set_ylabel("Average Occupancy (%)")
ax.set_xlabel("Day of Week")
ax.set_ylim(0, 70)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=8.5)
ax.legend(frameon=True, loc="upper right", fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_eda_weekday.png"), dpi=300)
plt.close()

# 3. Cleaning Boundary Illustration
raw_occ = (raw_df["Occupancy"] / raw_df["Capacity"]) * 100.0
clean_occ = all_clean["occupancy_pct"]

fig, ax = plt.subplots(figsize=(6.2, 3.8))
sns.kdeplot(raw_occ, ax=ax, color="#e11d48", linestyle="--", lw=1.8, label="Raw Telemetry (Unclipped with Anomaly Spikes)")
sns.kdeplot(clean_occ, ax=ax, color="#059669", lw=2.0, label="Cleaned Data (Bounded strictly to [0%, 100%])")
ax.axvline(0, color="#64748b", linestyle=":", lw=1.0)
ax.axvline(100, color="#64748b", linestyle=":", lw=1.0)
ax.axvline(50, color="#d97706", linestyle="-.", lw=1.0, label="Target Thresholds (50% & 80%)")
ax.axvline(80, color="#d97706", linestyle="-.", lw=1.0)
ax.set_xlabel("Occupancy Level (% of Capacity)")
ax.set_ylabel("Probability Density")
ax.set_xlim(-15, 120)
ax.legend(frameon=True, loc="upper right", fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_cleaning_boundary.png"), dpi=300)
plt.close()

print("Generated additional EDA and cleaning figures successfully.")
