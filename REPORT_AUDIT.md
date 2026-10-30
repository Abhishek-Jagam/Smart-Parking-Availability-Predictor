# Project Report Audit & Evidence Map

**Project Title:** Smart Parking Availability Predictor (ParkWise)  
**Dataset:** UCI Machine Learning Repository — Parking Birmingham (ID: 482)  
**Course:** Machine Learning Laboratory (B.Tech CSE — Mini Project, 15 Marks)  
**Audit Timestamp:** October 30, 2026

---

## 1. Project Summary & Core Architecture

| Dimension | Specification & Workspace Reality |
| :--- | :--- |
| **Problem** | Short-term occupancy forecasting across 30 municipal car parks to mitigate driver circling time, fuel wastage, and congestion. |
| **Dataset** | Authentic UCI Birmingham Car Park Occupancy dataset (`data/raw/dataset.csv`). 35,717 records recorded at ~30-min intervals between 07:30 and 16:34 from Oct 4 to Dec 19, 2016. CC BY 4.0 licence. |
| **Target Formulation** | 3-class classification 1-step ahead ($\sim 30\text{--}60$ minutes into the future):<br>• **Available:** Occupancy $< 50\%$<br>• **Nearly Full:** $50\% \le \text{Occupancy} < 80\%$<br>• **Full:** Occupancy $\ge 80\%$ |
| **Feature Pipeline** | 15 past-only engineered features: `Capacity`, `occupancy_pct`, `hour`, `minute`, `dayofweek`, `is_weekend`, `weekofyear`, `hour_sin`, `hour_cos`, `SystemCodeNumber_enc`, `lag_1` ($t-1$), `lag_2` ($t-2$), `lag_3` ($t-3$), `rolling_mean_3`, `rolling_std_3`. |
| **Data Split** | Strict chronological split (zero-leakage):<br>• **Train:** Oct 4 – Nov 27, 2016 (24,766 samples, $70\%$)<br>• **Val:** Nov 27 – Dec 8, 2016 (5,307 samples, $15\%$)<br>• **Test:** Dec 8 – Dec 19, 2016 (5,308 samples, $15\%$) |
| **Models Trained** | 11 models benchmarked: Persistence Baseline, Logistic Regression, Gaussian Naive Bayes, Artificial Neural Network (MLP), Support Vector Machine (RBF), K-Nearest Neighbors ($k=7$), Decision Tree, Random Forest (Winner), AdaBoost, plus XGBoost and LightGBM baselines. |
| **Production Model** | Balanced Random Forest Classifier (100 estimators, max depth 12). Validation Macro F1 = 0.9617, Accuracy = 0.9646. Test Accuracy = 0.9606, Test Macro F1 = 0.9564, Full Class Recall = 0.9421. |
| **UI Framework** | Streamlit (`app/main.py` + `app/helpers.py` + `app/styles.css`): Consumer-focused parking companion ("ParkWise") with single-flow search, status cards, 30-facility status board, busy time strips, and collapsed technical appendix. |
| **Deployment Method** | Docker container (`Dockerfile` with healthcheck on port 8501) and local Streamlit runner (`streamlit run app/main.py`). |

---

## 2. Existing Artifacts & Empirically Verified Metrics

All values below originate directly from executed scripts and serialized files in the workspace. **Zero estimated or fabricated numbers.**

### 2.1 Tabular Evaluation Metrics (`results/metrics.csv`)
*Evaluated on chronological validation set ($N = 5,307$):*

| Model | Val Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Recall (Full) | Recall (Nearly Full) | ROC-AUC (OvR) | Train Time (s) | Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Persistence Baseline** | 0.8839 | 0.8767 | 0.8752 | 0.8760 | 0.8838 | 0.8974 | 0.8001 | N/A | 0.000 | 0.010 |
| **Logistic Regression** | 0.9416 | 0.9358 | 0.9443 | 0.9397 | 0.9416 | 0.9844 | 0.9089 | 0.9911 | 0.413 | 0.000 |
| **Naive Bayes** | 0.8057 | 0.7924 | 0.7988 | 0.7951 | 0.8074 | 0.8484 | 0.6992 | 0.9375 | 0.012 | 0.000 |
| **ANN (MLP)** | 0.9587 | 0.9543 | 0.9572 | 0.9557 | 0.9588 | 0.9728 | 0.9292 | 0.9962 | 12.406 | 0.001 |
| **SVM (RBF Kernel)** | 0.9520 | 0.9464 | 0.9489 | 0.9473 | 0.9517 | 0.9782 | 0.8958 | 0.9950 | 21.573 | 0.223 |
| **KNN ($k=7$)** | 0.9261 | 0.9221 | 0.9154 | 0.9185 | 0.9256 | 0.9191 | 0.8519 | 0.9823 | 0.052 | 0.058 |
| **Decision Tree** | 0.9559 | 0.9528 | 0.9518 | 0.9523 | 0.9560 | 0.9510 | 0.9305 | 0.9713 | 0.197 | 0.001 |
| **Random Forest (Winner)**| **0.9646** | **0.9616** | **0.9618** | **0.9617** | **0.9646** | **0.9697** | **0.9371** | **0.9966** | **0.427** | **0.008** |
| **AdaBoost** | 0.9254 | 0.9212 | 0.9144 | 0.9175 | 0.9254 | 0.8919 | 0.8820 | 0.9789 | 1.916 | 0.005 |
| **XGBoost Baseline** | 0.9650 | 0.9627 | 0.9605 | 0.9616 | 0.9649 | 0.9635 | 0.9325 | 0.9972 | 0.518 | 0.002 |
| **LightGBM Baseline** | 0.9657 | 0.9624 | 0.9630 | 0.9627 | 0.9657 | 0.9736 | 0.9351 | 0.9970 | 0.228 | 0.003 |

*Held-out Unseen Test Metrics (`models/model_metadata.json`):*
- Test Accuracy: **0.9606** (96.06%)
- Test Macro F1: **0.9564** (95.64%)
- Test Recall (Full Class): **0.9421** (94.21%)
- Test Recall (Nearly Full): **0.9407** (94.07%)

### 2.2 Serialized Files & Model Artifacts
- `models/parking_model.joblib`: Serialized Balanced Random Forest classifier (100 estimators, max depth 12).
- `models/scaler.joblib`: Fitted `StandardScaler` (fit on train split only).
- `models/model_metadata.json`: Feature list, label mapping, facility capacities, and complete performance dictionary.
- `data/processed/train.csv`: 24,766 rows $\times$ 21 columns.
- `data/processed/val.csv`: 5,307 rows $\times$ 21 columns.
- `data/processed/test.csv`: 5,308 rows $\times$ 21 columns.

### 2.3 Publication Plots Already Generated (300 DPI)
- `results/figures/model_comparison_bars.png`: Multi-metric bar chart comparing Accuracy, Macro F1, and Recall (Full) across models.
- `results/figures/confusion_matrices_grid.png`: $2 \times 2$ normalized confusion matrix grid comparing Random Forest, XGBoost, Decision Tree, and MLP.
- `results/figures/roc_curves.png`: Multi-class One-vs-Rest (OvR) ROC curves with micro/macro AUC scores ($>0.99$).
- `results/figures/feature_importances.png`: Gini importance ranking for top predictors (`occupancy_pct`, `lag_1`, `rolling_mean_3`, `lag_2`, `Capacity`).

### 2.4 Verified Literature Artifacts (`docs/LITERATURE_LOG.md`)
5 verified peer-reviewed papers (2022–2024) confirmed via official CrossRef REST API:
1. Zhang et al. (2024), *ISPRS IJGI*, DOI: `10.3390/ijgi13050151` (MAT-LSTM Attention Network).
2. Enríquez et al. (2024), *Appl. Syst. Innov.*, DOI: `10.3390/asi7030052` (Fog Computing & ML Occupancy).
3. Dia et al. (2022), *Network*, DOI: `10.3390/network2020015` (Comparative ML on Street Parking).
4. Dahiya et al. (2024), *J. Adv. Transp.*, DOI: `10.1155/2024/8474973` (IoT Ensemble Classifiers).
5. Wong et al. (2023), *Sensors*, DOI: `10.3390/s23156869` (Vision & Sensor Fusion Review).

---

## 3. What is Missing for the Final Report

To ensure the 10-page report meets university submission standards without relying on placeholder text or assumptions, the following items must be noted or executed:

| Item | Current Status | Recommended Action for Report |
| :--- | :--- | :--- |
| **Exploratory Data Analysis (EDA) Figures** | Embedded in executed notebook `01_data_cleaning_eda.ipynb`, but not exported as standalone PNG files in `results/figures/`. | Export standalone 300-DPI PNGs for: (1) Hourly occupancy profile, (2) Day-of-week occupancy trends, and (3) Feature correlation heatmap. |
| **Feature Ablation Study** | Implicit in feature importance plot, but no explicit table quantifying drop in Macro F1 when removing temporal vs. lag features. | Run a quick ablation script: baseline vs. without lags vs. without temporal features, to provide an empirical discussion in Section 5. |
| **UI Screenshots in Repo** | User provided live browser screenshots during chat (`media_*.png`), but repo does not have cropped, high-resolution figures stored in `results/figures/` or `docs/`. | Save clean UI captures of ParkWise Home screen and Status Board into `results/figures/ui_home.png` and `ui_status_board.png` for Section 7. |
| **Neural Network Loss Curves** | MLP was trained via scikit-learn `MLPClassifier` with final metrics, but loss iteration curve was not saved to disk. | Extract `loss_curve_` from `MLPClassifier` and plot training convergence for Section 5/6 discussion. |

---

## 4. Proposed Final Heading List (Strictly Adhering to Compulsory Headings)

This proposed structure preserves the compulsory 8 headings in their exact order and title, while inserting logical subheadings and supplementary sections to cover every aspect of the university rubric:

```markdown
1. Introduction
   1.1 Problem Statement and Motivation
   1.2 Objectives and Scope of Smart Parking Prediction
   1.3 Real-World Telemetry: The Birmingham Municipal Context
2. Literature Review
   2.1 Overview of IoT-Driven Smart Parking Systems
   2.2 Deep Learning vs. Classical Machine Learning in Parking Telemetry
   2.3 Analysis of 5 State-of-the-Art Studies (2022–2024)
   2.4 Critical Synthesis and Comparative Literature Matrix
3. Methodology
   3.1 End-to-End System Architecture
   3.2 Feature Formulation and Leakage Prevention Framework
   3.3 Target Availability Definition and Classification Thresholds
   3.4 Model Selection and Evaluation Strategy
4. Data Cleaning and Preprocessing
   4.1 Dataset Characteristics (UCI Birmingham Parking)
   4.2 Telemetry Cleaning and Anomaly Correction (Clipping & Deduplication)
   4.3 Feature Engineering (Temporal Cycles, Past-Only Lags, Rolling Aggregations)
   4.4 Chronological Splitting (70/15/15) vs. Random Splitting Leakage Analysis
   4.5 Class Imbalance Mitigation (Class Weights Formulation)
5. Results and Discussion
   5.1 Exploratory Occupancy Dynamics (Diurnal & Day-of-Week Patterns)
   5.2 In-Depth Evaluation of the Winning Model (Balanced Random Forest)
   5.3 Confusion Matrix Analysis and Error Breakdown
   5.4 Feature Importance and Interpretability (Gini Index)
   5.5 Feature Ablation Analysis
6. State-of-the-Art Models Comparison
   6.1 Experimental Benchmark Setup (8 Syllabus Models + Baselines)
   6.2 Comprehensive Performance Leaderboard (Accuracy, F1, Recall, Latency)
   6.3 ROC-AUC Multi-Class Diagnostic Analysis
   6.4 Computational Efficiency, Latency, and Edge Viability
   6.5 Selection Justification for Urban Decision Support
7. User Interface Development and Deployment
   7.1 Consumer-Centric Design Philosophy ("ParkWise")
   7.2 Streamlit Web Application Architecture and Navigation
   7.3 Dynamic Decision Support: Alternative Facilities and Arrival Windows
   7.4 Accessibility (WCAG AA) and Cross-Platform Responsiveness
   7.5 Containerized Deployment (Docker and Cloud Readiness)
8. References
   [Complete verified citations with real DOIs and peer-reviewed venues]

[OPTIONAL APPENDICES / CLOSING SECTIONS]
9. Conclusion and Future Scope
   9.1 Summary of Findings
   9.2 Limitations (Missing GPS, Weather Factors)
   9.3 Future Directions (Edge Deployment, Multi-Modal Vision Fusion)
```

