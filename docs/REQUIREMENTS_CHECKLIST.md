# Final Requirements Verification & Checklist

This matrix cross-references every requirement against verifiable file paths and outputs in this repository.

---

## Evaluation Rubric Verification Matrix (15 Marks)

| Part | Component | Max Marks | Status | File-Path Evidence |
| :--- | :--- | :---: | :---: | :--- |
| **1** | **Data Cleaning & Splitting** | **3** | ✅ Verified | `src/preprocess.py`<br>`data/raw/dataset.csv` (35,717 rows, Birmingham)<br>`data/processed/train.csv` (24,766 rows)<br>`data/processed/val.csv` (5,307 rows)<br>`data/processed/test.csv` (5,308 rows)<br>`notebooks/01_data_cleaning_eda.ipynb` |
| **2** | **State-of-the-Art Model Comparison & Analytics** | **4** | ✅ Verified | `src/train.py`<br>`results/metrics.csv` (11 models compared)<br>`results/figures/model_comparison_bars.png`<br>`results/figures/confusion_matrices_grid.png`<br>`results/figures/feature_importances.png`<br>`results/figures/roc_curves.png`<br>`models/parking_model.joblib`<br>`models/model_metadata.json`<br>`notebooks/02_model_training_comparison.ipynb`<br>`notebooks/03_best_model_export.ipynb` |
| **3** | **UI Deployment & Cross-Platform Accessibility** | **4** | ✅ Verified | `app/main.py` (5 screens: Predict, Status Board, Insights, Model Performance, About)<br>`app.py` (root loader)<br>`.streamlit/config.toml` (navy + teal corporate theme)<br>`Dockerfile` (container deployment fallback) |
| **4** | **Code Quality, Repo & Viva Documentation** | **4** | ✅ Verified | `tests/test_pipeline.py` (4/4 pytest passing)<br>`README.md`<br>`docs/DECISIONS.md`<br>`docs/PROGRESS.md`<br>`docs/VIVA_GUIDE.md`<br>`requirements.txt` |

---

## Detailed Requirement Audit

1. **Dataset Compliance:**
   - [x] Used ONLY `data/raw/dataset.csv` (UCI Parking Birmingham dataset: 30 car parks, 35,717 records, Oct–Dec 2016, 08:00–16:30).
   - [x] Sourced under CC BY 4.0 licence; no web crawling or data fabrication.
   - [x] No artificial coordinates invented; map screen replaced by city-wide **Facility Status Board**.

2. **Data Cleaning & Splitting:**
   - [x] Clipped negative occupancies (12 cases) and overflow values exceeding physical capacity (373 cases).
   - [x] Deduplicated readings on `(SystemCodeNumber, LastUpdated)`.
   - [x] Past-only feature engineering: hour, minute, day of week, weekend, week of year, cyclical sine/cosine hour, car park ID encoder, 3 autoregressive lags ($t-1, t-2, t-3$), and rolling mean/std.
   - [x] Zero-leakage chronological split ($70\% / 15\% / 15\%$).

3. **Model Benchmark & Analytics:**
   - [x] Benchmarked all 8 syllabus algorithms (Exp 9): Logistic Regression, Naive Bayes, MLP, SVM, KNN, Decision Tree, Random Forest, AdaBoost.
   - [x] Evaluated modern gradient boosting baselines: XGBoost and LightGBM.
   - [x] Evaluated Persistence Baseline ($t \to t+1$).
   - [x] Metrics logged: Accuracy, Precision (Macro/Weighted), Recall (Macro/Weighted), Recall on Full and Nearly Full, ROC-AUC (OvR), train time, inference time.
   - [x] Printed confusion matrices for all models.
   - [x] Random Forest selected and justified: Test Accuracy $0.9606$, Test Macro F1 $0.9564$, Test Recall(Full) $0.9421$.
   - [x] 300-DPI publication figures generated in `results/figures/`.

4. **Colab Notebooks:**
   - [x] `01_data_cleaning_eda.ipynb`
   - [x] `02_model_training_comparison.ipynb`
   - [x] `03_best_model_export.ipynb`
   - [x] Clean local execution verified via nbconvert with outputs saved.

5. **Frontend UI:**
   - [x] Modern corporate aesthetic: navy (`#0f172a`) and teal (`#0ea5e9`), clean typography, whitespace.
   - [x] 5 screens: Predict, Status Board, Insights, Model Performance, About.
   - [x] Operating hours validation (07:00–17:00) with friendly messages, cached models (`@st.cache_resource`), zero traceback leaks.
