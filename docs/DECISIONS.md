# Engineering Decisions & Technical Log

This document records architectural, mathematical, and data engineering decisions made throughout the development of the Smart Parking Availability Predictor.

---

## 1. Dataset Selection: Real Birmingham Car Park Occupancy Data

### Decision
The project uses the authentic **Parking Birmingham** dataset (`data/raw/dataset.csv`), published via the UC Irvine Machine Learning Repository under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence.
- **Period:** October 4, 2016 – December 19, 2016 (Autumn/Winter, 11 operating weeks)
- **Scope:** 30 municipal and NCP-operated car parks across Birmingham, UK
- **Volume:** 35,717 raw observation records recorded between 08:00 and 16:30 at ~30-minute intervals
- **Original Attributes:** `SystemCodeNumber`, `Capacity`, `Occupancy`, `LastUpdated`

### Justification
Using this real dataset provides authentic physical dynamics (sensor errors, missing updates, morning rushes, shopping spikes, weekend dips). Unlike synthetic data, it satisfies university requirements for working with real-world open telemetry.

---

## 2. Target Variable & Threshold Formulation

### Decision
A 3-class classification target predicting car park availability status **1 step ahead (~30 to 60 minutes into the future)** was adopted:
- **Available:** Occupancy $< 50\%$
- **Nearly Full:** Occupancy $\ge 50\%$ and $< 80\%$
- **Full:** Occupancy $\ge 80\%$

### Justification
1. **Industry Alignment:** This 3-tier partitioning follows standard municipal traffic guidance (e.g., Variable Message Signs / VMS):
   - $< 50\%$ indicates abundant spaces available.
   - $50\% - 79\%$ indicates medium to high utilization; drivers can enter but should anticipate searching.
   - $\ge 80\%$ indicates the lot is near operational saturation; practical capacity is constrained by aisle maneuvering.
2. **Empirical Class Balance:** In the Birmingham dataset, the distribution is:
   - Available: $\approx 53.6\%$
   - Nearly Full: $\approx 31.8\%$
   - Full: $\approx 14.6\%$
   This naturally provides a realistic multi-class classification challenge where identifying the critical "Nearly Full" and "Full" classes is vital to prevent driver queuing and urban congestion.

---

## 3. Data Cleaning & Anomaly Correction

### Decision
1. **Negative Occupancy:** Sensor telemetry contained 12 readings with negative values (down to $-8$). These anomalies were clipped to $0$.
2. **Occupancy Exceeding Capacity:** 373 records had occupancy greater than rated capacity (up to $104.1\%$), caused by overflow bay usage or temporary double-parking. To prevent unbounded percentages, occupancy was bounded to rated capacity ($\min(\text{Occupancy}, \text{Capacity})$).
3. **Deduplication:** Duplicate records on `(SystemCodeNumber, LastUpdated)` were removed, retaining the first valid entry.
4. **Chronological Sorting:** The dataset was grouped and sorted strictly by `SystemCodeNumber` and `LastUpdated` ascending.

---

## 4. Feature Engineering (Past-Only, Zero Lookahead)

### Decision
All features are derived strictly from historical and present timestamps:
1. **Temporal Features:**
   - `hour`, `minute`: Captures daily commute and shopping patterns
   - `dayofweek`: 0 (Monday) to 6 (Sunday)
   - `is_weekend`: Binary flag ($1$ for Saturday/Sunday, $0$ for Weekdays)
   - `weekofyear`: Captures seasonal trends heading into the December holiday period
   - `hour_sin`, `hour_cos`: Cyclical trigonometric transformations of the diurnal cycle
2. **Spatial / Metadata:**
   - `Capacity`: Physical size of the facility (ranging from 220 to 4,675 spaces)
   - `SystemCodeNumber_enc`: Categorical car park identifier encoded via `LabelEncoder` (fit on train only)
3. **Autoregressive Temporal Lags (per Car Park):**
   - `lag_1`: Occupancy percentage 1 step prior (~30 mins ago)
   - `lag_2`: Occupancy percentage 2 steps prior (~60 mins ago)
   - `lag_3`: Occupancy percentage 3 steps prior (~90 mins ago)
4. **Rolling Statistics (per Car Park):**
   - `rolling_mean_3`: Moving average over the previous 3 readings
   - `rolling_std_3`: Moving standard deviation over the previous 3 readings (sensor volatility)

---

## 5. Leakage-Free Chronological Splitting

### Decision
Data was partitioned chronologically across all car parks:
- **Train Split (70%):** October 4, 2016 – November 23, 2016 (24,769 samples)
- **Validation Split (15%):** November 23, 2016 – December 6, 2016 (5,308 samples)
- **Test Split (15%):** December 6, 2016 – December 19, 2016 (5,308 samples)

### Justification
Random cross-validation on time-series telemetry causes severe data leakage: readings from adjacent minutes leak into test sets, resulting in deceptively inflated performance. Chronological splitting ensures models are evaluated on unseen future calendar weeks.

---

## 6. Preprocessing & Class Imbalance Handling

### Decision
1. Feature scaling (`StandardScaler`) is fit strictly on the training set and applied downstream to validation and test splits inside scikit-learn pipelines.
2. Class weights (`class_weight='balanced'`) are utilized during model training to ensure the model does not ignore the minority "Full" class ($14.6\%$).

---

## 7. Model Selection & Viva Justification

### Decision
The **Random Forest Classifier** was selected as the optimal production model over 9 evaluated competitors (Logistic Regression, Gaussian NB, MLP, SVM, KNN, Decision Tree, AdaBoost, XGBoost, LightGBM).

### Justification
- **Macro F1:** Balances precision and recall across all three classes without skew toward the majority "Available" class.
- **Recall on "Full" and "Nearly Full":** Essential for practical city operations—drivers must be warned before arriving at a saturated parking facility.
- **Inference Latency:** Sub-millisecond execution ($< 1$ ms per sample) makes it ideal for lightweight web dashboard deployment without expensive GPU dependencies.

---

## 8. Frontend Architecture: Status Board vs Map

### Decision
Because the authentic Birmingham dataset contains no spatial GPS latitude/longitude coordinates (only system codes and names), we avoided fabricating artificial coordinates. Instead, the UI incorporates a real-time **Facility Status Board** presenting color-coded status badges, capacities, live occupancy percentages, and forecast cards for each of the 30 car parks.

---

## 9. Consumer-Centric Streamlit UI Redesign ("ParkWise")

### Decision
Redesigned the frontend from an analyst/data-science dashboard into a consumer-facing parking companion named **ParkWise** ("Know before you go"):
1. **One question, one answer:** The home screen answers: *"Where are you going and when?"* with instant plain-language status cards and at most 3 visible inputs.
2. **Plain Language Only:** Eliminated ML jargon (`Class 2`, `F1`, `ROC-AUC`, `Confidence 0.81`). Converted statuses into driver-friendly verdicts: `Easy to park`, `Filling up`, `Likely full`, with intuitive fill levels ("About 85% full") and estimated space counts ("~150 spaces left").
3. **Actionable Recommendations:** Created `app/helpers.py` to evaluate the model across alternative car parks and hourly windows. If a car park is likely full, ParkWise immediately suggests the best alternative facility and optimal arrival window.
4. **Accessible Visual Style:** Navy + teal palette with emerald, amber, and rose used strictly for status and always paired with accessible symbols (`●`, `▲`, `■`) for WCAG AA compliance. Mobile-first width constraint (680px max-width) and zero horizontal scrolling.
5. **Friendly Facility Names:** Mapped raw alphanumeric system codes (`BHMBCCMKT01`, `BHMNCPHST01`) to recognizable landmark names ("Markets Car Park", "NCP High Street").
6. **Academic Rigor Preservation:** Preserved model comparison tables, confusion matrices, ROC curves, and feature importance figures inside a collapsed section ("For the curious / project details") under the About screen for laboratory viva grading.
