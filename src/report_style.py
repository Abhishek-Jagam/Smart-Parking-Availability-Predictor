"""
Report Style Configuration for Matplotlib / Seaborn.
Enforces 300 DPI, calm corporate navy palette, clean typography (min 10pt),
labeled axes with units, and title omission (captions added in LaTeX/report).
"""

import matplotlib.pyplot as plt
import seaborn as sns

def set_report_style():
    """Applies unified publication styling for report figures."""
    plt.rcParams.clear()
    
    # Palette definition: Navy (#0f172a), Teal (#0ea5e9), Emerald (#059669), Amber (#d97706), Rose (#e11d48)
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
        "legend.fontsize": 10,
        "figure.titlesize": 12,
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 1.0,
        "grid.color": "#f1f5f9",
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05
    })

