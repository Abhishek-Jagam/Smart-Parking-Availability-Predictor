"""
Generates verified figures and benchmark tables for Section 6: State-of-the-Art Models Comparison.
Evaluates at least 4 diverse models on the EXACT SAME chronological split and preprocessing:
1. Classical Baseline: Logistic Regression (L2 penalty)
2. Support Vector Machine: SVC (RBF kernel, scaled features)
3. Deep Learning / Neural Network: Multi-Layer Perceptron (MLP: 64x32 hidden layers, ReLU, Adam)
4. Decision Tree Baseline: CART (max depth 8)
5. Gradient Boosting Ensemble: XGBoost (100 estimators, learning rate 0.1)
6. Modern Light Gradient Boosting: LightGBM (100 estimators)
7. Winning Tree Ensemble: Balanced Random Forest (100 estimators, max depth 12)

Records:
- Accuracy, Macro F1, Weighted F1, Macro Precision, Macro Recall
- Training Time (s), Inference Latency per sample (ms)
- Parameter Count / Complexity Metric
Saves to report/tables/model_comparison.csv
Plots clean, 300 DPI bar chart comparison to report/figures/sota_model_comparison.png
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# Ensure src is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.report_style import set_report_style

FEATURE_COLS = [
    "Capacity", "occupancy_pct", "hour", "minute", "dayofweek",
    "is_weekend", "weekofyear", "hour_sin", "hour_cos", "SystemCodeNumber_enc",
    "lag_1", "lag_2", "lag_3", "rolling_mean_3", "rolling_std_3"
]


def count_parameters(model, model_type: str, n_features: int, n_classes: int) -> int:
    """Calculates or estimates the parameter count / capacity for each architecture."""
    if model_type == "Logistic Regression":
        # weights: (n_classes * n_features) + intercepts: (n_classes)
        return (n_classes * n_features) + n_classes
    elif model_type == "Decision Tree":
        # node count in the tree
        return model.tree_.node_count
    elif model_type == "Random Forest":
        # total node count across all 100 decision trees
        return sum(tree.tree_.node_count for tree in model.estimators_)
    elif model_type == "Multi-Layer Perceptron (MLP)":
        # (15*64 + 64) + (64*32 + 32) + (32*3 + 3)
        return (15 * 64 + 64) + (64 * 32 + 32) + (32 * 3 + 3)
    elif model_type == "Support Vector Machine (RBF)":
        # Number of support vectors * features + dual coefficients
        return model.support_vectors_.shape[0] * n_features
    elif model_type == "XGBoost":
        # 100 trees * 3 classes * avg 31 nodes
        return 100 * 3 * 31
    elif model_type == "LightGBM":
        # 100 trees * 3 classes * max 31 leaves
        return 100 * 3 * 31
    return 0


def generate_section6_artifacts():
    set_report_style()
    
    fig_dir = os.path.join(BASE_DIR, "report", "figures")
    tab_dir = os.path.join(BASE_DIR, "report", "tables")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)
    
    # Load identical processed splits
    train_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "train.csv"))
    val_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "val.csv"))
    test_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "test.csv"))
    
    label_map = {"Available": 0, "Nearly Full": 1, "Full": 2}
    y_train = train_df["target_class"].map(label_map).values
    y_val = val_df["target_class"].map(label_map).values
    y_test = test_df["target_class"].map(label_map).values
    
    X_train_raw = train_df[FEATURE_COLS].values
    X_val_raw = val_df[FEATURE_COLS].values
    X_test_raw = test_df[FEATURE_COLS].values
    
    # Fit scaler strictly on Train
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_val_scaled = scaler.transform(X_val_raw)
    X_test_scaled = scaler.transform(X_test_raw)
    
    models = [
        ("Logistic Regression (L2)", LogisticRegression(max_iter=1000, random_state=42), True, "Logistic Regression"),
        ("Decision Tree (CART)", DecisionTreeClassifier(max_depth=8, random_state=42), False, "Decision Tree"),
        ("Support Vector Machine (RBF)", SVC(kernel="rbf", C=1.0, probability=True, random_state=42), True, "Support Vector Machine (RBF)"),
        ("Multi-Layer Perceptron (MLP)", MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42, early_stopping=True), True, "Multi-Layer Perceptron (MLP)"),
        ("XGBoost Classifier", xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="mlogloss"), False, "XGBoost"),
        ("LightGBM Classifier", lgb.LGBMClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbose=-1), False, "LightGBM"),
        ("Random Forest (Winning Model)", RandomForestClassifier(n_estimators=100, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1), False, "Random Forest")
    ]
    
    results = []
    
    for name, clf, needs_scaling, model_type in models:
        X_tr = X_train_scaled if needs_scaling else X_train_raw
        X_te = X_test_scaled if needs_scaling else X_test_raw
        
        # Measure Training Time
        t0 = time.perf_counter()
        clf.fit(X_tr, y_train)
        train_time = time.perf_counter() - t0
        
        # Measure Latency (1,000 samples)
        sample_subset = X_te[:1000]
        t_lat0 = time.perf_counter()
        _ = clf.predict(sample_subset)
        lat_ms = ((time.perf_counter() - t_lat0) / 1000.0) * 1000.0
        
        # Evaluation on Held-Out Test Set
        y_pred = clf.predict(X_te)
        y_proba = clf.predict_proba(X_te)
        
        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro")
        f1_weighted = f1_score(y_test, y_pred, average="weighted")
        
        # Recall specifically on minority Full class (Class 2)
        rec_full = recall_score(y_test, y_pred, labels=[2], average=None)[0]
        
        # ROC-AUC (OvR)
        auc_score = roc_auc_score(y_test, y_proba, multi_class="ovr")
        
        # Parameter Count
        param_count = count_parameters(clf, model_type, n_features=len(FEATURE_COLS), n_classes=3)
        
        results.append({
            "Model Architecture": name,
            "Family": model_type,
            "Test Accuracy": round(acc, 4),
            "Macro Precision": round(prec_macro, 4),
            "Macro Recall": round(rec_macro, 4),
            "Macro F1": round(f1_macro, 4),
            "Weighted F1": round(f1_weighted, 4),
            "Recall (Full Class)": round(rec_full, 4),
            "ROC-AUC (OvR)": round(auc_score, 4),
            "Training Time (s)": round(train_time, 3),
            "Inference Latency (ms)": round(lat_ms, 3),
            "Parameters / Capacity": f"{param_count:,}"
        })
        
    res_df = pd.DataFrame(results)
    res_df.to_csv(os.path.join(tab_dir, "model_comparison.csv"), index=False)
    
    # ---------------------------------------------------------
    # Plot: Clean 300 DPI Horizontal Comparison Chart
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    y_pos = np.arange(len(results))
    height = 0.35
    
    f1_vals = [r["Macro F1"] for r in results]
    rec_vals = [r["Recall (Full Class)"] for r in results]
    labels = [r["Model Architecture"].split(" (")[0] for r in results]
    
    ax.barh(y_pos - height/2, f1_vals, height, label="Macro F1-Score", color="#0ea5e9", edgecolor="#0284c7")
    ax.barh(y_pos + height/2, rec_vals, height, label="Recall on 'Full' Saturated Bays", color="#0f172a", edgecolor="#020617")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("Held-Out Test Metric Score")
    ax.set_xlim(0.80, 1.0)
    ax.legend(frameon=True, loc="lower right", fontsize=9.0)
    
    for i in range(len(results)):
        ax.text(f1_vals[i] + 0.002, y_pos[i] - height/2, f"{f1_vals[i]:.3f}", va="center", fontsize=8.0)
        ax.text(rec_vals[i] + 0.002, y_pos[i] + height/2, f"{rec_vals[i]:.3f}", va="center", fontsize=8.0)
        
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "sota_model_comparison.png"), dpi=300)
    plt.close()
    
    print("Section 6 SOTA model comparison artifacts generated successfully.")


if __name__ == "__main__":
    generate_section6_artifacts()

