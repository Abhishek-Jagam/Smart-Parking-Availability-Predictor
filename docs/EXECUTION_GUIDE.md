# End-to-End Execution & Model Functionality Guide
**Project:** Smart Parking Availability Predictor (University ML Lab Mini Project — 15 Marks)  
**Dataset:** UCI Birmingham Parking Dataset (35,717 records across 30 municipal car parks, Oct–Dec 2016)  
**Production Model:** Balanced Random Forest Classifier (100 estimators, max depth 12)  

---

## Overview of the Pipeline

To make the predictive model fully functional from scratch, the system follows a 6-phase pipeline:
```
[Raw CSV: data/raw/dataset.csv]
          │
          ▼
[1. Preprocessing & Feature Engineering] ──► Generates data/processed/{train,val,test}.csv
          │
          ▼
[2. Model Training & Evaluation] ────────► Generates models/parking_model.joblib, metrics.csv, figures
          │
          ▼
[3. Automated Verification & Tests] ────► Ensures 100% test pass (pytest)
          │
          ▼
[4. Interactive UI Launch] ─────────────► Serves Streamlit dashboard at http://localhost:8501
```

---

## Step 1: Environment Setup

Ensure Python 3.10+ (tested on Python 3.12) is installed. Open PowerShell or a terminal in the project root:

```powershell
cd c:\Users\Asus\OneDrive\Desktop\Smart-Parking-Availability-Predictor-main
```

### 1.1 (Optional but Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 1.2 Install Required Dependencies
Install the pinned libraries specified in `requirements.txt`:
```powershell
pip install -r requirements.txt
```
*(If default PyPI times out, install via a fast mirror: `pip install -r requirements.txt -i https://pypi.org/simple`)*

---

## Step 2: Verify Raw Dataset

Verify that the authentic UCI Birmingham Parking dataset is present:
- Location: `data/raw/dataset.csv`
- Shape: 35,717 rows, 4 raw columns (`SystemCodeNumber`, `Capacity`, `Occupancy`, `LastUpdated`).

You can verify it with this one-liner:
```powershell
python -c "import pandas as pd; df=pd.read_csv('data/raw/dataset.csv'); print('Dataset verified:', df.shape)"
```

---

## Step 3: Run Data Preprocessing & Feature Engineering

Run `src/preprocess.py` to clean anomalies, compute leak-free lag/rolling features, and split the data chronologically:

```powershell
python src/preprocess.py
```

### What this script does automatically:
1. **Cleaning:** Removes sensor overflow artifacts (negative occupancy or occupancy > capacity) and deduplicates timestamps.
2. **Feature Engineering (15 features):**
   - Temporal: `hour`, `minute`, `day_of_week`, `is_weekend`, `sin_hour`, `cos_hour`.
   - Facility: `SystemCodeNumber_encoded`, `Capacity`.
   - Historical Past Lags: `lag_1` ($t-1$), `lag_2` ($t-2$), `lag_3` ($t-3$).
   - Rolling Aggregations: `rolling_mean_3`, `rolling_std_3`, `rolling_min_3`, `rolling_max_3`.
3. **Target Variable Definition:**
   - 1-step ahead occupancy classification ($\sim 30\text{--}60$ minutes into the future):
     - `Available`: Occupancy $< 50\%$
     - `Nearly Full`: $50\% \le \text{Occupancy} < 80\%$
     - `Full`: Occupancy $\ge 80\%$
4. **Leak-Free Chronological Split:**
   - **Train:** Oct 4, 2016 – Nov 27, 2016 (24,766 rows)
   - **Validation:** Nov 27, 2016 – Dec 8, 2016 (5,307 rows)
   - **Test:** Dec 8, 2016 – Dec 19, 2016 (5,308 rows)

---

## Step 4: Train & Benchmark All Models

Run `src/train.py` to train all 11 model configurations, benchmark performance, pick the winner, and serialize artifacts:

```powershell
python src/train.py
```

### Models Evaluated:
1. **Persistence Baseline** (Naive prior status check)
2. **Logistic Regression**
3. **Gaussian Naive Bayes**
4. **K-Nearest Neighbors (KNN)**
5. **Decision Tree**
6. **Support Vector Classifier (LinearSVC)**
7. **Multi-Layer Perceptron (MLP Neural Net)**
8. **AdaBoost**
9. **Random Forest (Balanced)** — **WINNER** ($\text{Macro } F_1 = 0.9564$, Full Class Recall $= 94.2\%$)
10. **XGBoost Classifier**
11. **LightGBM Classifier**

### Outputs Generated:
- Model Weights: `models/parking_model.joblib`
- Normalizer: `models/scaler.joblib`
- Metadata: `models/model_metadata.json`
- Metrics Log: `results/metrics.csv`
- Publication Figures (300 DPI):
  - `results/figures/model_comparison_bars.png`
  - `results/figures/confusion_matrices_grid.png`
  - `results/figures/roc_curves.png`
  - `results/figures/feature_importances.png`

---

## Step 5: (Optional) Re-Execute Jupyter Notebooks

All 3 Colab-ready notebooks can be executed headlessly or opened in Jupyter Lab / Google Colab:

```powershell
# Execute 01: Data Cleaning & EDA
jupyter nbconvert --to notebook --execute notebooks/01_data_cleaning_eda.ipynb --inplace

# Execute 02: Model Training & Comparison
jupyter nbconvert --to notebook --execute notebooks/02_model_training_comparison.ipynb --inplace

# Execute 03: Best Model Export & Pipeline Validation
jupyter nbconvert --to notebook --execute notebooks/03_best_model_export.ipynb --inplace
```

---

## Step 6: Automated Test Verification

Run the test suite to verify data integrity, feature pipeline invariants, and inference determinism:

```powershell
python -m pytest tests/ -v
```
**Expected Result:** `4 passed in ~0.5s` (100% pass rate).

---

## Step 7: Launch the Streamlit Frontend

Start the production UI:

```powershell
streamlit run app/main.py
```
*(Alternatively, you can run `streamlit run app.py`)*

### Accessing the Web Application:
- Open your browser at: `http://localhost:8501`
- **Tabs Available:**
  1. **Predict:** Select car park, date, time, and recent occupancy to get instant multi-class probability breakdown and status.
  2. **Facility Status Board:** Live grid of all 30 Birmingham municipal car parks colour-coded by forecasted state.
  3. **Insights:** Exploratory hourly trends and peak congestion patterns.
  4. **Model Performance:** Real-time metrics table, confusion matrix grid, ROC curves, and feature importance rankings.
  5. **About:** Project methodology, data provenance, and grading rubric alignment.

---

## Step 8: (Optional) Docker Deployment

To run the entire system inside a sandboxed Docker container:

```bash
# Build the Docker image
docker build -t smart-parking-app .

# Run the container mapping port 8501
docker run -p 8501:8501 smart-parking-app
```
Then navigate to `http://localhost:8501`.

---

## Quick Reference Summary

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Install** | `pip install -r requirements.txt` | Install runtime libraries |
| **Preprocess** | `python src/preprocess.py` | Clean data & engineer 15 features |
| **Train** | `python src/train.py` | Benchmark 11 models & save best weights |
| **Test** | `python -m pytest tests/` | Run automated test suite |
| **Run UI** | `streamlit run app/main.py` | Launch interactive web application |

