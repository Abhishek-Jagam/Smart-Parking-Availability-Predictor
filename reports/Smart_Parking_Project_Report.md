# ACADEMIC PROJECT REPORT

## SMART PARKING AVAILABILITY PREDICTOR USING MACHINE LEARNING

---

### **A Mini-Project Report Submitted in Partial Fulfillment of the Requirements for the Award of the Degree of**

### **BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING**

**Course:** Machine Learning Laboratory (Semester V)  
**Course Code:** CS504P / ML-LAB  
**Academic Year:** 2026–2027  

**Submitted by:**  
- **Student Name:** [Your Name / Team Members]  
- **Roll Number(s):** [Your Roll Number]  
- **Batch:** B1  

**Under the Guidance of:**  
[Faculty Guide / Laboratory Mentor Name]  
Assistant Professor, Department of Computer Science & Engineering  

**Department of Computer Science and Engineering**  
[College / University Name]  
[City, State, PIN Code]  

---

## CERTIFICATE

This is to certify that the mini-project titled **"Smart Parking Availability Predictor Using Machine Learning"** submitted by **[Your Name]** (Roll No: **[Your Roll Number]**) to the Department of Computer Science and Engineering, is a bonafide record of work carried out under my supervision in partial fulfillment of the requirements for the Semester V Machine Learning Laboratory evaluation (15 Marks) for the academic year 2026–2027.

<br><br>

---------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ----------------------------------  
**Internal Guide / Mentor** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of the Department (CSE)**  

---

## 1. ABSTRACT

Urban parking searching accounts for up to 30% of metropolitan traffic congestion, exacerbating carbon emissions, driver stress, and fuel wastage. This mini-project presents an end-to-end Machine Learning system that predicts on-street parking availability one hour into the future across 420 urban parking block segments. Utilizing the landmark historical **SFpark** sensor dataset comprising 5,080,320 observations recorded at 5-minute intervals, we formulate a 3-class classification problem: **Available** (< 50% occupancy), **Nearly Full** (50% to 79% occupancy), and **Full** (80% to 100% occupancy). 

Strict chronological train-validation-test splitting is implemented to completely prevent temporal data leakage. We engineer same-segment historical lag features (15, 30, and 60 minutes) and temporal context variables (hour of day, weekday, weekend flag). In accordance with Experiment 9 of the Machine Learning Lab syllabus, eight classification algorithms are trained and systematically evaluated: Logistic Regression, Naive Bayes, Multi-Layer Perceptron (ANN), Support Vector Machine (RBF), K-Nearest Neighbors, Decision Tree, Random Forest, and AdaBoost, benchmarked against a persistence baseline. 

The **Random Forest Classifier** achieved the highest validation macro F1-score of **0.744** (test macro F1: **0.736**, accuracy: **74.8%**), outperforming the persistence baseline (macro F1: 0.729). Critically, for the high-cost error where a truly full street is misclassified as available, Random Forest achieved an error rate of under 3.5% (only 255 out of 7,191 test cases). An interactive, cross-platform Streamlit dashboard was deployed providing time-slot parking outlooks, smart-city color telemetry, and CSV reporting.

---

## 2. INTRODUCTION & MOTIVATION

Searching for curb parking in dense urban environments is a primary contributor to urban bottlenecks, safety hazards, and environmental pollution. Traditional parking applications merely report static parking garage locations or display current occupancy data that is already obsolete by the time a commuter arrives at the destination.

Predictive machine learning models bridge this latency gap. By learning regular human commuting routines, hourly diurnal trends, and short-term neighborhood occupancy decay, an ML system can forecast parking segment states 30 to 60 minutes in advance.

### 2.1 Motivation & Objectives
1. **Practical Predictive Horizon:** Forecast availability 60 minutes ahead so drivers can make informed route decisions before embarking on journeys.
2. **Standardized Class Definitions:** Define intuitive status tiers:
   - **Available:** 0% to 49% occupancy (ample parking).
   - **Nearly Full:** 50% to 79% occupancy (filling up, search required).
   - **Full:** 80% to 100% occupancy (critical congestion, avoidance advised).
3. **Rigorous Syllabus Alignment:** Fulfill the Semester V ML Lab curriculum by comparing 8 foundational classifiers alongside hyperparameter tuning, leakage prevention, and model persistence.
4. **Interactive Accessibility:** Deploy an intuitive web application providing instant forecasts across time slots.

---

## 3. SYSTEM ARCHITECTURE & WORKFLOW

The following diagram illustrates the complete leak-free data processing and model inference architecture:

```mermaid
flowchart TD
    A[Raw SFpark data.csv\n5,080,320 rows, 332 MB] --> B[Data Inspection & Delimiter Detection\nSemicolon Delimiter]
    B --> C[Filter Capacity = 0\n494,235 invalid rows dropped]
    C --> D[Chronological Segment Grouping\nSort by segmentid & timestamp]
    D --> E[Feature Engineering\nLag 15m, 30m, 60m + Hour, Weekday, Weekend]
    E --> F[60-Min Future Target Alignment\nLead 12 readings ahead within segment]
    F --> G[Hourly Sampling & Missing Lag Removal\nFinal N = 364,122 rows]
    G --> H[Strict Chronological Split\nTrain: 70% | Val: 15% | Test: 15%]
    H --> I[Train 8 Classifiers + Persistence Baseline]
    I --> J[Macro F1 & Confusion Matrix Evaluation]
    J --> K[Hyperparameter Tuning via TimeSeriesSplit]
    K --> L[Export Model & Metadata\njoblib.dump]
    L --> M[Interactive Streamlit Dashboard\nTime-Slot Predictor & Visuals]
```

---

## 4. DATASET DESCRIPTION & PREPROCESSING

### 4.1 SFpark Dataset Characteristics
The experiment utilizes the official open-access **SFpark** sensor dataset recorded across San Francisco between **13 June 2013 and 24 July 2013 (42 days)**:
- **Raw Rows:** 5,080,320
- **Total Columns:** 24 (4 core documented columns + 20 unverified `observed` / `diff` columns)
- **Delimitation:** Semicolon (`;`)
- **File Size:** ~332 MB (332,406,705 bytes)
- **Distinct Parking Segments:** 420

| Column Name | Data Type | Physical Meaning | Used in ML Pipeline |
| :--- | :--- | :--- | :--- |
| `timestamp` | `datetime64[ns]` | Date and time of sensor reading (5-min frequency) | Yes (time feature extraction) |
| `segmentid` | `int32` | Unique identifier of city parking block segment | Yes (segment grouping) |
| `capacity` | `int16` | Number of legal parking bays in the segment | Yes (dynamic capacity feature) |
| `occupied` | `int16` | Number of bays currently occupied | Yes (calculating occupancy %) |
| `observed1..10`, `diff1..10` | `float32` | Undocumented auxiliary sensor readings (mostly empty) | No (excluded for scientific integrity) |

### 4.2 Data Cleaning & Integrity Verification
1. **Zero-Capacity Rows:** 494,235 rows (9.7%) have `capacity = 0`. Calculating occupancy percentage `(occupied / capacity) * 100` would trigger division by zero. These rows represent road work, temporary street sweeping closures, or unmonitored segments. They were discarded without inventing artificial capacity.
2. **Missing & Duplicate Values:** Across the core columns in positive capacity rows, missing values = 0, exact duplicate records = 0, and duplicate `(timestamp, segmentid)` pairs = 0.
3. **Physical Constraints:** Confirmed that `0 <= occupied <= capacity` holds for 100% of usable records.
4. **Outlier Treatment:** An IQR test on capacity flags 7 street segments exceeding 22.5 bays. These were verified as legitimate large downtown blocks and retained. Occupancy of 100% occurs in 8.5% of readings, representing genuine peak demand.

---

## 5. FEATURE ENGINEERING & TARGET FORMULATION

### 5.1 Same-Segment Historical Lag Features
Parking demand exhibits strong auto-regressive momentum. To capture velocity and acceleration of occupancy changes without data leakage, we compute historical lag features strictly within each parking segment:
- Consecutive sensor readings are recorded every **5 minutes**.
- **Lag 15 min:** Shift $t - 3$ periods within segment.
- **Lag 30 min:** Shift $t - 6$ periods within segment.
- **Lag 60 min:** Shift $t - 12$ periods within segment.

### 5.2 60-Minute Future Target Construction
The prediction target is the occupancy class observed **12 readings ahead ($t + 12$ periods = 60 minutes)**:

$$\text{Occupancy \%} = \left(\frac{\text{occupied}}{\text{capacity}}\right) \times 100$$

$$\text{Class} = \begin{cases} 
0 \text{ (Available)} & \text{if } \text{Occupancy \%} < 50\% \\
1 \text{ (Nearly Full)} & \text{if } 50\% \le \text{Occupancy \%} < 80\% \\
2 \text{ (Full)} & \text{if } \text{Occupancy \%} \ge 80\%
\end{cases}$$

### 5.3 Leakage Prevention & Hourly Sampling
To prevent adjacent time autocorrelation (where 10:00 AM and 10:05 AM are nearly identical), the modeling dataset is sampled at 1 reading per segment per hour. This reduces the modeling pool to **364,122 rows**:
- **Available:** 149,736 rows (41.1%)
- **Nearly Full:** 142,426 rows (39.1%)
- **Full:** 71,960 rows (19.8%)

Full is the minority class; hence `class_weight='balanced'` was utilized across supported estimators.

---

## 6. CHRONOLOGICAL TRAIN-VALIDATION-TEST METHODOLOGY

In time-series parking prediction, standard randomized cross-validation is invalid because it uses future points to predict the past (temporal leakage). We establish strict chronological boundaries:

| Split Partition | Row Count | Date Range Covered | Purpose |
| :--- | :--- | :--- | :--- |
| **Train Set** | 233,021 | 13 Jun 2013 to 09 Jul 2013 | Pipeline fitting & model training |
| **Validation Set** | 58,249 | 09 Jul 2013 to 16 Jul 2013 | Model comparison & tuning |
| **Test Set** | 72,852 | 16 Jul 2013 to 24 Jul 2013 | Final held-out evaluation (evaluated once) |

---

## 7. EVALUATION METRICS & MATHEMATICAL FORMULAS

Given class imbalance (Full is ~20%), overall accuracy alone is misleading. We evaluate models using **Macro-Averaged F1-Score**:

### 7.1 Accuracy
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

### 7.2 Precision and Recall
$$\text{Precision}_c = \frac{TP_c}{TP_c + FP_c}, \quad \text{Recall}_c = \frac{TP_c}{TP_c + FN_c}$$

### 7.3 Class F1-Score and Macro F1-Score
$$F1_c = 2 \times \frac{\text{Precision}_c \times \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}$$

$$\text{Macro } F1 = \frac{1}{C} \sum_{c=1}^{C} F1_c \quad \text{where } C = 3$$

---

## 8. MODEL COMPARISON & PERFORMANCE ANALYTICS (EXPERIMENT 9)

All eight required syllabus classifiers and the persistence baseline were evaluated on the exact same chronological validation set:

| Rank | Model Name | Validation Accuracy | Validation Macro F1 | Recall (Full Class) | Academic Performance Summary |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Random Forest (Selected)** | **0.753** | **0.744** | **0.74** | **Best overall non-linear ensemble; superior balance** |
| 2 | Persistence Baseline ($t \to t+60$) | 0.752 | 0.740 | 0.72 | Extremely strong benchmark due to smooth occupancy drift |
| 3 | Support Vector Machine (RBF) | 0.747 | 0.738 | 0.71 | Effective non-linear decision boundary; slow training |
| 4 | AdaBoost Classifier | 0.747 | 0.732 | 0.70 | Adaptive boosting on decision stumps |
| 5 | Decision Tree Classifier | 0.740 | 0.730 | 0.69 | Highly explainable; prone to slight variance |
| 6 | K-Nearest Neighbors (KNN, k=7) | 0.742 | 0.726 | 0.67 | Instance-based clustering; sensitive to feature scales |
| 7 | Logistic Regression | 0.729 | 0.717 | 0.64 | Linear hyperplanes struggle with non-linear transitions |
| 8 | Artificial Neural Net (MLP) | 0.696 | 0.679 | 0.59 | Requires extensive tuning; sub-optimal convergence |
| 9 | Naive Bayes (Gaussian) | 0.435 | 0.412 | 0.38 | Fails due to severe violation of feature independence |

### 8.1 Key Viva Observation: Why Naive Bayes Fails
Gaussian Naive Bayes achieved only **41.2% Macro F1**. Naive Bayes assumes all features are conditionally independent:

$$P(X_1, X_2, X_3 | Y) = P(X_1 | Y) \cdot P(X_2 | Y) \cdot P(X_3 | Y)$$

In our dataset, `occ_lag_15`, `occ_lag_30`, and `occ_lag_60` have Pearson correlation coefficients above $0.85$. This extreme multi-collinearity causes severe probability over-counting, degrading classification accuracy.

---

## 9. HYPERPARAMETER TUNING & FINAL TEST EVALUATION

### 9.1 Hyperparameter Optimization via TimeSeriesSplit
Using 3-fold chronological cross-validation (`TimeSeriesSplit`), we tuned the top candidates:
- **Decision Tree:** `max_depth=8`, `min_samples_leaf=5` $\to$ Macro F1: **0.740**.
- **Support Vector Machine:** `C=1.0`, `kernel='rbf'` $\to$ Macro F1: **0.734**.
- **Random Forest:** `n_estimators=100`, `max_depth=12`, `min_samples_leaf=2` $\to$ Macro F1: **0.743**.

### 9.2 Final Evaluation on Held-Out Test Set (Evaluated Once)
The tuned **Random Forest Pipeline** was evaluated on the unseen chronological test set (72,852 records):
- **Test Accuracy:** **0.748 (74.8%)**
- **Test Macro Precision:** **0.730**
- **Test Macro Recall:** **0.745**
- **Test Macro F1-Score:** **0.736**
- *Persistence Baseline Comparison on Test:* Accuracy **0.743**, Macro F1 **0.729**.

### 9.3 Critical Confusion Matrix Analysis
In urban parking management, classification errors have asymmetric costs:
- **Harmless Error:** Predicting Nearly Full when Available (driver arrives and is pleasantly surprised).
- **Critical High-Cost Error:** Predicting **Available** when the street is actually **Full**. A commuter travels to the spot only to find zero spaces, leading to traffic jams and road frustration.

**Test Set Confusion Matrix for 7,191 truly Full cases:**
- Predicted Full: **5,324** (Recall = 74.0%)
- Predicted Nearly Full: **1,612** (Driver is cautioned)
- Predicted Available (Critical Error): **255 only (3.5%)**

---

## 10. INTERACTIVE STREAMLIT DASHBOARD & DEPLOYMENT

The project features a responsive web application (`app.py`):
1. **Segment Selection:** Allows selecting any of the 420 SFpark segments with pre-configured legal capacities.
2. **Dual Input Modes:** Supports automatic loading of SFpark diurnal hourly averages or direct slider-based live sensor inputs.
3. **Multi-Slot Prediction Timeline:** Projects availability for **Now, T+15, T+30, T+45, T+60 (ML Target), T+90, and T+120 minutes**.
4. **Smart-City Color Indicators:** High-contrast color cards and pill badges:
   - 🟢 Available (`#10b981`)
   - 🟡 Nearly Full (`#f59e0b`)
   - 🔴 Full (`#ef4444`)
5. **Data Export:** Enables real-time CSV download of forecasts for municipal parking management.
6. **Cross-Platform Readiness:** Runs in modern web browsers across Windows, macOS, Linux, iOS, and Android.

---

## 11. PROJECT LIMITATIONS & FUTURE SCOPE

### 11.1 Limitations (Honest Scientific Disclosure for Viva)
1. **Geographical & Seasonal Specificity:** Data reflects San Francisco streets during summer 2013; patterns may not generalize to Indian university campuses without local re-training.
2. **Exogenous Features Absent:** The dataset lacks weather conditions (rain reduces walking tolerance), holidays (July 4th anomaly), and local events (concerts, baseball games).
3. **Coarse Segment Capacities:** With a median capacity of 8 bays, the movement of a single vehicle shifts occupancy by 12.5%, introducing inherent discrete variance.

### 11.2 Future Scope
1. Ingest real-time IoT magnetic sensor or camera-based parking feeds.
2. Incorporate live weather APIs (OpenWeatherMap) and city holiday/event calendars.
3. Extend multi-horizon predictions using recurrent architectures (LSTM) or gradient boosting (XGBoost / LightGBM).

---

## 12. CONCLUSION

This mini-project successfully developed, evaluated, and deployed a machine learning-based Smart Parking Availability Predictor. By strictly avoiding temporal data leakage through chronological splitting and segment-bound lag engineering, the system provides reliable 60-minute forecasts. The Random Forest classifier demonstrated superior multi-class balance with an accuracy of **74.8%** and a Macro F1 of **0.736**, while minimizing dangerous false-available errors to under 3.5%. The accompanying Streamlit interface and comprehensive evaluation artifacts fully meet the requirements of the Semester V Machine Learning practical curriculum.

---

## 13. REFERENCES
1. SFpark Project Open Data Archive: *San Francisco Municipal Transportation Agency (SFMTA)*. https://doi.org/10.7910/DVN/YLWCSU
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.
4. Streamlit Documentation: *A faster way to build and share data apps*. https://docs.streamlit.io/
