# Reproduction Guide: Report Artifacts & Benchmark Experiments
**Project:** Smart Parking Availability Predictor (ParkWise)  
**Verification Level:** 100% Empirically Executed (Zero Estimated Values)  
**Python Version:** Python 3.12+ (Windows / Linux / macOS)  

---

## 1. Environment Setup

Install all pinned dependencies:
```bash
pip install -r requirements.txt
```

---

## 2. Generate Section 4: Data Cleaning & Preprocessing Artifacts

Executes telemetry cleaning checks, chronological split audits, and generates 300-DPI distribution plots:
```bash
python src/generate_section4.py
```

### Outputs Generated:
- `report/tables/dataset_splits.csv` (Sample counts, percentage, and date boundaries)
- `report/tables/data_cleaning_audit.csv` (Negative readings, overflow anomalies, duplicates before vs after)
- `report/tables/feature_engineering_registry.csv` (All 15 engineered features, datatypes, scaling, and descriptions)
- `report/tables/class_distribution_summary.csv` (Class frequencies across splits and balanced loss weights)
- `report/figures/target_class_distribution.png` (300 DPI bar chart of target proportions across splits)
- `report/figures/sensor_boundary_cleaning.png` (300 DPI density plot of raw unbounded readings vs. clipped clean data)

---

## 3. Generate Section 5: Results and Discussion Artifacts

Evaluates the production Balanced Random Forest model on the held-out test split, computes PR curves, estimator convergence, real error samples, and performs feature ablation:
```bash
python src/generate_section5.py
```

### Outputs Generated:
- `report/tables/test_per_class_metrics.csv` (Precision, Recall, F1, and Support per category on held-out test set)
- `report/tables/error_analysis_cases.csv` (4 real, verified failure cases with physical root causes)
- `report/tables/feature_ablation_study.csv` (Performance degradation without lags, rolling stats, or cyclical hour)
- `report/figures/production_confusion_matrix.png` (300 DPI normalized confusion matrix with raw counts)
- `report/figures/precision_recall_curves.png` (300 DPI multi-class PR curves with AUC-PR scores)
- `report/figures/rf_training_validation_curve.png` (300 DPI training vs. validation Macro F1 across n_estimators)

---

## 4. Generate Section 6: State-of-the-Art Models Comparison

Trains and evaluates 7 diverse model architectures on the **exact same chronological split** and **identical preprocessing pipeline**:
```bash
python src/generate_section6.py
```

### Outputs Generated:
- `report/tables/model_comparison.csv` (Full benchmark table with Accuracy, Macro F1, Recall (Full), Latency, Training Time, and Parameter Counts)
- `report/figures/sota_model_comparison.png` (300 DPI clean horizontal comparison chart)

---

## 5. Automated Verification

Run pytest to ensure all test assertions pass:
```bash
python -m pytest tests/ -v
```
Expected result: `4 passed in ~0.5s` (100% pass rate).

