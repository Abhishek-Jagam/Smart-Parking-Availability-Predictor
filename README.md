# Smart Parking Availability Predictor Using Machine Learning

> **B.Tech Computer Science & Engineering — Machine Learning Laboratory Mini Project (15 Marks)**  
> **Dataset:** Real UCI Parking Birmingham Telemetry (30 Municipal & NCP Car Parks, CC BY 4.0)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-v1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.30%2B-red.svg)](https://streamlit.io/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## 📌 Project Overview
Urban parking search contributes to over 30% of metropolitan downtown traffic congestion. This project implements an end-to-end Machine Learning pipeline that predicts car park availability 30 to 60 minutes into the future across 30 major car parks in Birmingham, UK.

The target availability status is categorized into 3 actionable municipal tiers:
- **Available:** Occupancy $< 50\%$
- **Nearly Full:** Occupancy $50\% - 79.9\%$
- **Full / Saturated:** Occupancy $\ge 80\%$

---

## 🎯 15-Mark Evaluation Rubric Mapping

| Rubric Component | Marks | Deliverable Assets | Implementation Highlights |
| :--- | :---: | :--- | :--- |
| **Part 1: Data Cleaning & Splitting** | **3 Marks** | `src/preprocess.py`<br>`notebooks/01_data_cleaning_eda.ipynb` | Bounded physical occupancy clipping ($[0, \text{Capacity}]$), deduplication, past-only lag ($t-1, t-2, t-3$) and rolling feature engineering, leak-free chronological splitting ($70/15/15$). |
| **Part 2: Model Comparison & Analytics** | **4 Marks** | `src/train.py`<br>`notebooks/02_model_training_comparison.ipynb`<br>`notebooks/03_best_model_export.ipynb` | Comprehensive benchmark across **all 8 syllabus classifiers** (Experiment 9) + Persistence Baseline + XGBoost & LightGBM. Printed confusion matrices, 300-DPI publication figures, model serialization. |
| **Part 3: UI Deployment & Accessibility** | **4 Marks** | `app/main.py`<br>`Dockerfile`<br>`.streamlit/config.toml` | Interactive Streamlit operations dashboard: Single facility prediction, City Status Board (all 30 facilities), Temporal Insights, Model Performance, responsive layout, friendly operational validation. |
| **Part 4: Code Quality & Submission** | **4 Marks** | `tests/test_pipeline.py`<br>`docs/DECISIONS.md`<br>`docs/VIVA_GUIDE.md`<br>`requirements.txt` | Modular `src/` architecture, automated `pytest` test suite, strict zero-leakage verification, comprehensive 25-question viva examination guide. |

---

## 📊 Benchmark Comparison Table (Chronological Validation Set)

Evaluated on the exact chronological validation set (5,307 samples, Nov 26 – Dec 8, 2016):

| Model Name | Validation Accuracy | Macro F1 | Weighted F1 | Recall (Full Class) | Recall (Nearly Full) | Inference Latency | Syllabus Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Random Forest (Selected)** | **0.9646** | **0.9617** | **0.9646** | **0.9697** | **0.9371** | **0.010 ms** | ⭐ **Best Multi-Class Balance** |
| LightGBM Baseline | 0.9657 | 0.9627 | 0.9657 | 0.9736 | 0.9351 | 0.004 ms | Modern Gradient Boosting |
| XGBoost Baseline | 0.9650 | 0.9616 | 0.9649 | 0.9635 | 0.9325 | 0.002 ms | Modern Gradient Boosting |
| Artificial Neural Net (MLP) | 0.9587 | 0.9557 | 0.9588 | 0.9728 | 0.9292 | 0.001 ms | Multi-Layer Perceptron |
| Decision Tree | 0.9559 | 0.9523 | 0.9560 | 0.9510 | 0.9305 | 0.000 ms | Tree Baseline (Exp 5) |
| Support Vector Machine (RBF) | 0.9520 | 0.9473 | 0.9517 | 0.9782 | 0.8958 | 0.345 ms | High-Margin Kernel Classifier |
| Logistic Regression | 0.9414 | 0.9396 | 0.9415 | 0.9844 | 0.9089 | 0.000 ms | Linear Baseline |
| K-Nearest Neighbors (KNN, k=7) | 0.9261 | 0.9185 | 0.9256 | 0.9191 | 0.8519 | 0.095 ms | Non-parametric Distance Metric |
| AdaBoost | 0.9254 | 0.9175 | 0.9254 | 0.8919 | 0.8820 | 0.009 ms | Adaptive Boosting Ensemble |
| Persistence Baseline ($t \to t+1$) | 0.8839 | 0.8760 | 0.8838 | 0.8974 | 0.8001 | 0.010 ms | Physical Autoregressive Anchor |
| Naive Bayes (Gaussian) | 0.8057 | 0.7951 | 0.8074 | 0.8484 | 0.6992 | 0.001 ms | Fails under lag collinearity |

### Final Held-Out Test Set Result (Dec 8 – Dec 19, 2016, Evaluated Once):
- **Accuracy:** `0.9606 (96.1%)`
- **Macro F1-Score:** `0.9564`
- **Recall on "Full" Class:** `0.9421 (94.2%)`
- **Recall on "Nearly Full" Class:** `0.9407 (94.1%)`

---

## 🏗️ Pipeline Architecture

```text
[Raw Birmingham Telemetry (35,717 rows)]
                   │
                   ▼
[Data Cleaning & Boundary Clipping: min(Occupancy, Capacity), Occupancy >= 0]
                   │
                   ▼
[Feature Engineering: Past-Only Lags (t-1, t-2, t-3), Rolling Mean/Std, Cyclical Hour]
                   │
                   ▼
[Chronological Partitioning: Train (70%) | Validation (15%) | Test (15%)]
                   │
                   ▼
[Model Benchmarking: 8 Syllabus Classifiers + Baselines with Class Balancing]
                   │
                   ▼
[Production Serialization: Random Forest joblib + Metadata JSON]
                   │
                   ▼
[Streamlit UI Dashboard: Predict, Status Board, Insights, Model Analytics]
```

---

## 🚀 How to Run Locally

### 1. Setup Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline End-to-End
```bash
# 1. Preprocess raw data
python src/preprocess.py

# 2. Train models and generate benchmark figures
python src/train.py

# 3. Run automated tests
python -m pytest tests/

# 4. Launch Streamlit UI
streamlit run app/main.py
```

---

## 🐳 Docker Container Deployment
```bash
docker build -t smart-parking-predictor .
docker run -p 8501:8501 smart-parking-predictor
```
Open `http://localhost:8501` in your browser.

---

## 👥 Project Team & Submission Details
- **Course:** B.Tech Computer Science & Engineering — Machine Learning Laboratory (Semester V)
- **Prepared By:** [Team Member 1], [Team Member 2], [Team Member 3]
- **Shared Sheet Submission Status:** [Report & Repository Links Pending Upload]
