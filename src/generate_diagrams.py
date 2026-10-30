"""
Generates Architecture Pipeline Diagram and SOTA Accuracy-vs-Latency chart
for the final report.
Outputs:
1. report/figures/methodology_pipeline.png (300 DPI)
2. report/figures/sota_accuracy_vs_latency.png (300 DPI)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure src is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.report_style import set_report_style

def generate_report_diagrams():
    set_report_style()
    fig_dir = os.path.join(BASE_DIR, "report", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    # -------------------------------------------------------------------
    # 1. Methodology Pipeline Flowchart Diagram (300 DPI)
    # -------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    
    # Box definition helper
    def draw_box(x, y, w, h, title, subtitle, bg_color="#f8fafc", edge_color="#0ea5e9"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            facecolor=bg_color,
            edgecolor=edge_color,
            linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.65, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0f172a")
        ax.text(x + w/2, y + h*0.30, subtitle, ha="center", va="center", fontsize=7.8, color="#475569")
        
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5, mutation_scale=12)
        )
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, ha="center", fontsize=7.2, color="#0ea5e9", fontweight="bold")

    # Step 1: Raw Telemetry
    draw_box(0.3, 3.2, 2.4, 1.4, "1. IoT Sensor Telemetry", "35,717 logs | 30 Car Parks\nLastUpdated, Capacity, Occupancy", "#f8fafc", "#64748b")
    draw_arrow(2.7, 3.9, 3.4, 3.9)
    
    # Step 2: Cleaning & Engineering
    draw_box(3.4, 3.2, 3.1, 1.4, "2. Cleaning & Feature Pipeline", "Clipped [0, Cap] | 15 Past Features\nLags (t-1,2,3), Rolling, Cycles", "#f0fdf4", "#059669")
    draw_arrow(6.5, 3.9, 7.2, 3.9)
    
    # Step 3: Leakage-Free Split
    draw_box(7.2, 3.2, 2.5, 1.4, "3. Chronological Split", "70% Train | 15% Val | 15% Test\nZero Time-Series Leakage", "#eff6ff", "#0ea5e9")
    draw_arrow(8.45, 3.2, 8.45, 2.1)
    
    # Step 4: SOTA Benchmarking
    draw_box(6.8, 0.7, 2.9, 1.4, "4. Multi-Model Benchmark", "11 Models Evaluated\nCost-Sensitive Balanced Loss", "#fefce8", "#d97706")
    draw_arrow(6.8, 1.4, 5.8, 1.4)
    
    # Step 5: Production Serialization
    draw_box(3.4, 0.7, 2.4, 1.4, "5. Best Model Serialization", "Balanced Random Forest\nMacro F1: 0.956 | Recall: 94.2%", "#eff6ff", "#0ea5e9")
    draw_arrow(3.4, 1.4, 2.7, 1.4)
    
    # Step 6: Consumer UI & Deployment
    draw_box(0.3, 0.7, 2.4, 1.4, "6. 'ParkWise' Companion", "Streamlit UI + Docker\nActionable Driver Guidance", "#fdf2f8", "#db2777")
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "methodology_pipeline.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------------
    # 2. SOTA Accuracy vs Inference Latency Scatter Plot (300 DPI)
    # -------------------------------------------------------------------
    tab_path = os.path.join(BASE_DIR, "report", "tables", "model_comparison.csv")
    if os.path.exists(tab_path):
        df = pd.read_csv(tab_path)
        
        fig, ax = plt.subplots(figsize=(6.5, 4.2))
        
        colors = ["#64748b", "#0284c7", "#e11d48", "#9333ea", "#059669", "#d97706", "#0f172a"]
        markers = ["o", "s", "^", "D", "v", "P", "*"]
        
        for i, row in df.iterrows():
            m_name = row["Model Architecture"].split(" (")[0]
            lat = row["Inference Latency (ms)"]
            f1 = row["Macro F1"]
            
            # Highlight Random Forest
            if "Random Forest" in m_name:
                ax.scatter(lat, f1, color="#0ea5e9", s=180, zorder=5, marker="*", edgecolors="#0f172a", lw=1.5, label="Random Forest (Winner)")
                ax.annotate(f"{m_name}\n(F1: {f1:.3f}, {lat:.3f} ms)", (lat + 0.005, f1 - 0.003), fontsize=8.5, fontweight="bold", color="#0f172a")
            else:
                ax.scatter(lat, f1, color=colors[i % len(colors)], s=75, zorder=4, marker=markers[i % len(markers)], label=m_name)
                # Position labels dynamically
                y_offset = 0.002 if i % 2 == 0 else -0.003
                ax.annotate(m_name, (lat + 0.005, f1 + y_offset), fontsize=8.0, color="#334155")
                
        ax.set_xlabel("Inference Latency per Sample (ms) [Log Scale Preferred]")
        ax.set_ylabel("Macro F1-Score on Held-Out Test Set")
        ax.set_ylim(0.915, 0.970)
        ax.set_xlim(-0.01, 0.25)
        ax.legend(frameon=True, loc="lower right", fontsize=8.0)
        
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "sota_accuracy_vs_latency.png"), dpi=300)
        plt.close()
        
    print("Methodology pipeline and accuracy-vs-latency diagrams generated successfully.")

if __name__ == "__main__":
    generate_report_diagrams()

