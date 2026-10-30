# Smart Parking Availability Predictor — Viva & Oral Examination Guide

This document prepares students for the viva voce and project demonstration for the 15-mark university ML Lab mini-project.

---

## 1. High-Yield Viva Questions & Answers

### Q1: What dataset did you use and what are its key properties?
**Answer:** We used the real-world **Parking Birmingham** dataset from the UC Irvine (UCI) Machine Learning Repository (CC BY 4.0). It contains 35,717 records across 30 municipal and NCP car parks in Birmingham, UK, recorded between October and December 2016 from 08:00 to 16:30 at ~30-minute intervals. The core attributes are `SystemCodeNumber`, `Capacity`, `Occupancy`, and `LastUpdated`.

### Q2: What is your target variable and how do you justify the thresholds?
**Answer:** We formulated a 3-class classification target predicting availability status 1 step ahead (~30 to 60 minutes):
- **Available:** $< 50\%$ occupancy
- **Nearly Full:** $50\% - 79.9\%$ occupancy
- **Full / Saturated:** $\ge 80\%$ occupancy
This aligns with municipal traffic management standards (Variable Message Signs). Below $50\%$ drivers find spots effortlessly; above $80\%$, aisle search time increases exponentially, causing queues and localized urban congestion.

### Q3: Why did you choose chronological splitting instead of random train_test_split?
**Answer:** In sensor and time-series telemetry, consecutive observations have high temporal autocorrelation. A random split causes severe **data leakage**, where a reading from 10:00 AM might be in the train set and 10:30 AM of the same day in the test set, creating artificially inflated accuracy. A chronological split (first 70% train, next 15% val, final 15% test) tests true generalizability on unseen future calendar weeks.

### Q4: Why did Random Forest win over models like SVM or Naive Bayes?
**Answer:** 
1. **Vs. Naive Bayes (F1: 0.9617 vs 0.7951):** Naive Bayes assumes conditional feature independence. Because autoregressive lags ($t-1, t-2, t-3$) are highly collinear, Gaussian NB fails.
2. **Vs. SVM (Latency: 0.010 ms vs 0.345 ms):** SVM with an RBF kernel has high computational complexity ($O(N^2)$ to $O(N^3)$), making training slow (32s vs 0.5s for RF) and real-time edge inference slower.
3. **Vs. Single Decision Tree:** Random forest averages 100 decorrelated trees, reducing variance and resisting localized sensor noise.

### Q5: Why is Accuracy alone an inadequate metric for this problem?
**Answer:** The classes are imbalanced: Available ($53.6\%$), Nearly Full ($31.8\%$), Full ($14.6\%$). A naive model could achieve high accuracy by mostly predicting "Available". In municipal parking, the cost of misclassification is asymmetric: predicting a Full facility is Available causes drivers to waste time and create traffic jams. Therefore, **Macro F1** and **Recall on the "Full" class** are our primary evaluation metrics.

### Q6: How do you prevent data leakage during feature engineering?
**Answer:**
1. All lag and rolling statistics per car park are computed exclusively from the past: `rolling_mean` uses `.shift(1)` so the current timestamp's value is excluded.
2. Feature scalers (`StandardScaler`) and categorical encoders are `fit()` exclusively on the training set and merely `transform()` the validation and test sets.

### Q7: What are the main limitations of this dataset?
**Answer:** 
1. **Seasonal Scope:** Data spans only autumn/winter (Oct–Dec 2016), so summer holiday patterns are absent.
2. **Operating Hours:** Observations are collected daytime only (08:00–16:30); nighttime parking behavior is not captured.
3. **No GPS Coordinates:** The dataset lacks geographical coordinates, so a spatial map would require fabricating coordinates; we built a city-wide Facility Status Board instead.

### Q8: How does the Streamlit UI load and run the model?
**Answer:** The Streamlit app uses `@st.cache_resource` to deserialize `parking_model.joblib` and `model_metadata.json` into memory once upon startup. When a user enters facility parameters and observation time, the app constructs the 15-feature input vector and executes `model.predict()` and `model.predict_proba()` in sub-millisecond latency without reloading from disk.

---

## 2. Walkthrough of the Codebase Architecture
- `src/preprocess.py`: Implements anomaly clipping ($[0, \text{Capacity}]$), lag extraction, and chronological split.
- `src/train.py`: Trains all 8 syllabus algorithms + modern baselines, prints confusion matrices, exports `results/metrics.csv` and 300-DPI figures.
- `app/main.py`: Interactive 5-screen operations dashboard with navy+teal aesthetic.
- `notebooks/`: Three self-contained Jupyter notebooks with Colab badges and executed cell outputs.
- `tests/test_pipeline.py`: Pytest suite validating shapes, absence of leakage, and inference.

