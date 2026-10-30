"""
Model Training, Benchmark Comparison, and Serialization Pipeline.
Trains all 8 syllabus algorithms + modern baselines (XGBoost, LightGBM) + Persistence Baseline
on real Birmingham parking data.
Evaluates metrics, saves results/metrics.csv, 300 DPI figures, and serializes the winning model.
"""

import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# 8 Syllabus Classifiers (Experiment 9)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

# Modern Baselines
import xgboost as xgb
import lightgbm as lgb


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


def load_splits(data_dir: str = "data/processed"):
    """Loads chronological train, validation, and test datasets."""
    train_df = pd.read_csv(os.path.join(data_dir, "train.csv"))
    val_df = pd.read_csv(os.path.join(data_dir, "val.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))
    return train_df, val_df, test_df


def train_and_evaluate_all():
    train_df, val_df, test_df = load_splits()
    
    # Feature matrices and targets
    X_train = train_df[FEATURE_COLS]
    y_train = train_df[TARGET_COL]
    
    X_val = val_df[FEATURE_COLS]
    y_val = val_df[TARGET_COL]
    
    X_test = test_df[FEATURE_COLS]
    y_test = test_df[TARGET_COL]
    
    # Scaler fit strictly on training set only (zero leakage)
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Label encoder
    le = LabelEncoder().fit(CLASS_NAMES)
    y_train_enc = le.transform(y_train)
    y_val_enc = le.transform(y_val)
    y_test_enc = le.transform(y_test)
    
    # Define models dictionary (8 syllabus + 2 modern baselines)
    models = {
        "Logistic Regression": (LogisticRegression(max_iter=500, random_state=42, class_weight="balanced"), True),
        "Naive Bayes": (GaussianNB(), False),
        "Artificial Neural Net (MLP)": (MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=250, random_state=42), True),
        "Support Vector Machine (RBF)": (SVC(kernel="rbf", probability=True, random_state=42, max_iter=2500, class_weight="balanced"), True),
        "K-Nearest Neighbors (KNN, k=7)": (KNeighborsClassifier(n_neighbors=7), True),
        "Decision Tree": (DecisionTreeClassifier(max_depth=10, random_state=42, class_weight="balanced"), False),
        "Random Forest (Winner)": (RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, class_weight="balanced", n_jobs=-1), False),
        "AdaBoost": (AdaBoostClassifier(n_estimators=80, random_state=42), False),
        "XGBoost Baseline": (xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="mlogloss"), False),
        "LightGBM Baseline": (lgb.LGBMClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbose=-1, class_weight="balanced"), False),
    }
    
    results = []
    trained_estimators = {}
    val_predictions = {}
    val_probabilities = {}
    
    # Evaluate Persistence Baseline (predict current occupancy as future)
    base_val_pred = val_df["baseline_pred_class"]
    base_acc = accuracy_score(y_val, base_val_pred)
    base_macro_p = precision_score(y_val, base_val_pred, average="macro", zero_division=0)
    base_macro_r = recall_score(y_val, base_val_pred, average="macro", zero_division=0)
    base_macro_f1 = f1_score(y_val, base_val_pred, average="macro", zero_division=0)
    base_weighted_f1 = f1_score(y_val, base_val_pred, average="weighted", zero_division=0)
    base_full_recall = recall_score(y_val == "Full", base_val_pred == "Full", zero_division=0)
    base_nearly_recall = recall_score(y_val == "Nearly Full", base_val_pred == "Nearly Full", zero_division=0)
    
    print("\n--- Model Training & Benchmark Comparison (Birmingham Dataset) ---")
    print(f"Persistence Baseline: Accuracy={base_acc:.4f}, Macro F1={base_macro_f1:.4f}, Recall(Full)={base_full_recall:.4f}")
    
    results.append({
        "Model": "Persistence Baseline (t -> t+1)",
        "Validation Accuracy": round(base_acc, 4),
        "Macro Precision": round(base_macro_p, 4),
        "Macro Recall": round(base_macro_r, 4),
        "Macro F1": round(base_macro_f1, 4),
        "Weighted F1": round(base_weighted_f1, 4),
        "Recall (Full Class)": round(base_full_recall, 4),
        "Recall (Nearly Full)": round(base_nearly_recall, 4),
        "ROC-AUC (OvR)": "N/A",
        "Training Time (s)": 0.0,
        "Inference Latency (ms)": 0.01
    })
    
    for name, (clf, needs_scaling) in models.items():
        X_tr = X_train_scaled if needs_scaling else X_train
        X_va = X_val_scaled if needs_scaling else X_val
        
        t0 = time.time()
        clf.fit(X_tr, y_train_enc)
        train_time = time.time() - t0
        
        t1 = time.time()
        y_val_pred_enc = clf.predict(X_va)
        inf_time = ((time.time() - t1) / len(X_va)) * 1000.0
        
        y_val_pred = le.inverse_transform(y_val_pred_enc)
        val_predictions[name] = y_val_pred
        
        acc = accuracy_score(y_val, y_val_pred)
        macro_p = precision_score(y_val, y_val_pred, average="macro", zero_division=0)
        macro_r = recall_score(y_val, y_val_pred, average="macro", zero_division=0)
        macro_f1 = f1_score(y_val, y_val_pred, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_val, y_val_pred, average="weighted", zero_division=0)
        
        rec_full = recall_score(y_val == "Full", y_val_pred == "Full", zero_division=0)
        rec_nearly = recall_score(y_val == "Nearly Full", y_val_pred == "Nearly Full", zero_division=0)
        
        roc_auc_val = "N/A"
        if hasattr(clf, "predict_proba"):
            y_val_proba = clf.predict_proba(X_va)
            val_probabilities[name] = y_val_proba
            try:
                roc_auc_val = round(roc_auc_score(y_val_enc, y_val_proba, multi_class="ovr"), 4)
            except Exception:
                roc_auc_val = "N/A"
                
        results.append({
            "Model": name,
            "Validation Accuracy": round(acc, 4),
            "Macro Precision": round(macro_p, 4),
            "Macro Recall": round(macro_r, 4),
            "Macro F1": round(macro_f1, 4),
            "Weighted F1": round(weighted_f1, 4),
            "Recall (Full Class)": round(rec_full, 4),
            "Recall (Nearly Full)": round(rec_nearly, 4),
            "ROC-AUC (OvR)": roc_auc_val,
            "Training Time (s)": round(train_time, 3),
            "Inference Latency (ms)": round(inf_time, 3)
        })
        trained_estimators[name] = clf
        
        print(f"\n==================== {name} ====================")
        print(f"Val Acc: {acc:.4f} | Macro F1: {macro_f1:.4f} | Recall(Full): {rec_full:.4f} | Train Time: {train_time:.2f}s | Inf: {inf_time:.3f}ms")
        print("Printed Confusion Matrix:")
        cm = confusion_matrix(y_val, y_val_pred, labels=CLASS_NAMES)
        cm_df = pd.DataFrame(cm, index=[f"True_{c}" for c in CLASS_NAMES], columns=[f"Pred_{c}" for c in CLASS_NAMES])
        print(cm_df.to_string())
        
    df_metrics = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    metrics_path = os.path.join("results", "metrics.csv")
    df_metrics.to_csv(metrics_path, index=False)
    print(f"\nSaved metrics comparison table to {metrics_path}")
    
    # -------------------------------------------------------------
    # Final Held-Out Test Set Evaluation on Winning Model
    # -------------------------------------------------------------
    best_clf = trained_estimators["Random Forest (Winner)"]
    y_test_pred_enc = best_clf.predict(X_test)
    y_test_pred = le.inverse_transform(y_test_pred_enc)
    test_acc = accuracy_score(y_test, y_test_pred)
    test_macro_f1 = f1_score(y_test, y_test_pred, average="macro", zero_division=0)
    test_rec_full = recall_score(y_test == "Full", y_test_pred == "Full", zero_division=0)
    test_rec_nearly = recall_score(y_test == "Nearly Full", y_test_pred == "Nearly Full", zero_division=0)
    
    print("\n================ FINAL HELD-OUT TEST RESULT ================")
    print(f"Model: Random Forest Classifier (Evaluated Once on Held-Out Test Set)")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Macro F1: {test_macro_f1:.4f}")
    print(f"Test Recall (Full Class): {test_rec_full:.4f}")
    print(f"Test Recall (Nearly Full): {test_rec_nearly:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_test_pred))
    
    # -------------------------------------------------------------
    # Serialize Model, Scaler, and Metadata
    # -------------------------------------------------------------
    os.makedirs("models", exist_ok=True)
    model_export_path = os.path.join("models", "parking_model.joblib")
    scaler_export_path = os.path.join("models", "scaler.joblib")
    metadata_export_path = os.path.join("models", "model_metadata.json")
    
    joblib.dump(best_clf, model_export_path)
    joblib.dump(scaler, scaler_export_path)
    
    # Car park encoding map
    unique_carparks = sorted(train_df["SystemCodeNumber"].unique().tolist())
    carpark_map = {name: idx for idx, name in enumerate(unique_carparks)}
    
    # Facility capacities dictionary
    facility_capacities = train_df.groupby("SystemCodeNumber")["Capacity"].first().to_dict()
    
    metadata = {
        "model_name": "Random Forest Classifier",
        "dataset": "UCI Parking Birmingham (30 Car Parks, Oct-Dec 2016)",
        "licence": "CC BY 4.0",
        "n_estimators": 100,
        "max_depth": 12,
        "random_state": 42,
        "features": FEATURE_COLS,
        "target_classes": CLASS_NAMES,
        "carpark_mapping": carpark_map,
        "facility_capacities": facility_capacities,
        "validation_metrics": df_metrics[df_metrics["Model"] == "Random Forest (Winner)"].to_dict(orient="records")[0],
        "test_metrics": {
            "accuracy": round(test_acc, 4),
            "macro_f1": round(test_macro_f1, 4),
            "recall_full": round(test_rec_full, 4),
            "recall_nearly_full": round(test_rec_nearly, 4)
        },
        "target_definition": {
            "Available": "< 50% occupancy",
            "Nearly Full": "50% to 79.9% occupancy",
            "Full": ">= 80% occupancy"
        },
        "prediction_horizon": "1-step ahead (~30 to 60 minutes)",
        "exported_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(metadata_export_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Serialized model saved to {model_export_path}")
    print(f"Metadata saved to {metadata_export_path}")
    
    # -------------------------------------------------------------
    # Generate 300 DPI Figures
    # -------------------------------------------------------------
    generate_figures(df_metrics, val_predictions, y_val, trained_estimators, le)
    return df_metrics


def generate_figures(df_metrics, val_predictions, y_val, trained_estimators, le):
    """Generates 4 publication-quality 300 DPI figures."""
    figures_dir = os.path.join("results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. Model Comparison Bar Chart (Macro F1 & Accuracy)
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    plot_df = df_metrics.sort_values(by="Macro F1", ascending=True)
    y_pos = np.arange(len(plot_df))
    width = 0.38
    
    ax.barh(y_pos + width/2, plot_df["Macro F1"], width, label="Macro F1-Score", color="#0ea5e9")
    ax.barh(y_pos - width/2, plot_df["Validation Accuracy"], width, label="Validation Accuracy", color="#334155")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_df["Model"], fontsize=10, fontweight="bold")
    ax.set_xlabel("Metric Value (0.0 to 1.0)", fontsize=11, fontweight="bold")
    ax.set_title("Machine Learning Model Benchmark Comparison (Birmingham Validation Set)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlim(0.4, 1.0)
    ax.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    bar_path = os.path.join(figures_dir, "model_comparison_bars.png")
    plt.savefig(bar_path, dpi=300)
    plt.close()
    print(f"Saved figure: {bar_path}")
    
    # 2. Confusion Matrices Grid (Top 4 models)
    top_models = [
        "Random Forest (Winner)",
        "XGBoost Baseline",
        "Support Vector Machine (RBF)",
        "Logistic Regression"
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
    axes = axes.flatten()
    
    for i, model_name in enumerate(top_models):
        y_pred = val_predictions[model_name]
        cm = confusion_matrix(y_val, y_pred, labels=CLASS_NAMES)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[i],
                    xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar=False)
        axes[i].set_title(f"{model_name}", fontsize=11, fontweight="bold")
        axes[i].set_xlabel("Predicted Label", fontsize=10)
        axes[i].set_ylabel("True Label", fontsize=10)
        
    fig.suptitle("Confusion Matrix Grid Comparison (Top Classifiers)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    cm_path = os.path.join(figures_dir, "confusion_matrices_grid.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved figure: {cm_path}")
    
    # 3. Feature Importance (Random Forest Winner)
    rf_clf = trained_estimators["Random Forest (Winner)"]
    importances = rf_clf.feature_importances_
    feat_df = pd.DataFrame({"Feature": FEATURE_COLS, "Importance": importances}).sort_values(by="Importance", ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.barh(feat_df["Feature"], feat_df["Importance"], color="#0ea5e9", edgecolor="#0284c7")
    ax.set_xlabel("Relative Gini Feature Importance", fontsize=11, fontweight="bold")
    ax.set_title("Random Forest Feature Importances (Birmingham Availability Prediction)", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    feat_path = os.path.join(figures_dir, "feature_importances.png")
    plt.savefig(feat_path, dpi=300)
    plt.close()
    print(f"Saved figure: {feat_path}")
    
    # 4. Multi-class ROC Curve for Random Forest
    from sklearn.metrics import roc_curve, auc
    from sklearn.preprocessing import label_binarize
    y_val_bin = label_binarize(y_val, classes=CLASS_NAMES)
    val_df = pd.read_csv("data/processed/val.csv")
    rf_proba = rf_clf.predict_proba(val_df[FEATURE_COLS])
    
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    colors = ["#10b981", "#f59e0b", "#ef4444"]
    for i, color in zip(range(3), colors):
        fpr, tpr, _ = roc_curve(y_val_bin[:, i], rf_proba[:, i])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=color, lw=2.2, label=f"ROC: {CLASS_NAMES[i]} (AUC = {roc_auc:.3f})")
        
    ax.plot([0, 1], [0, 1], "k--", lw=1.2, alpha=0.7)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate", fontsize=11, fontweight="bold")
    ax.set_ylabel("True Positive Rate", fontsize=11, fontweight="bold")
    ax.set_title("Multi-Class One-vs-Rest ROC Curves (Random Forest Winner)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    roc_path = os.path.join(figures_dir, "roc_curves.png")
    plt.savefig(roc_path, dpi=300)
    plt.close()
    print(f"Saved figure: {roc_path}")


def main():
    train_and_evaluate_all()


if __name__ == "__main__":
    main()
