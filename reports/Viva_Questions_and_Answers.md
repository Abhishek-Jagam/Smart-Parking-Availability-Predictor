# VIVA VOCE PREPARATION GUIDE: SMART PARKING PREDICTOR
## Semester V B.Tech CSE Machine Learning Laboratory Mini Project (15 Marks)

This guide contains **25 essential viva questions and student-friendly answers** designed to help you confidently explain your project to your lab examiner/mentor ("mam").

---

### Q1: What is the main objective of your mini-project?
**Answer:**  
The objective is to predict urban parking availability **60 minutes into the future** as one of three classes: **Available** (< 50% occupied), **Nearly Full** (50% to 79% occupied), or **Full** (80% to 100% occupied). This allows drivers to know parking availability before starting their journey, reducing congestion, fuel wastage, and emissions.

---

### Q2: Is this a supervised or unsupervised machine learning problem?
**Answer:**  
It is a **supervised multi-class classification** problem. It is supervised because each training record has both input features (current occupancy, lag features, time of day) and a known ground-truth target label (the parking class observed 60 minutes later). It is multi-class because the target has 3 distinct categories.

---

### Q3: Why did you predict 60 minutes ahead instead of predicting right now (0 minutes)?
**Answer:**  
Predicting current availability ($t = 0$) is trivial—it is just reading a sensor. In real-world driving, an average commuter takes 30 to 60 minutes to travel to a destination. By predicting **60 minutes ahead**, the model provides actionable intelligence that accounts for parking spaces filling up or emptying while the driver is en route.

---

### Q4: Which dataset did you use, and what is its format?
**Answer:**  
We used the historical **SFpark** sensor dataset from San Francisco (June to July 2013). It contains **5,080,320 rows** and 24 columns across 420 parking block segments. It is **semicolon-delimited (`;`)** and approximately 332 MB in size.

---

### Q5: Why did you only use 4 columns out of the 24 columns in the dataset?
**Answer:**  
The 4 core documented columns are `timestamp`, `segmentid`, `capacity`, and `occupied`. The remaining 20 columns (`observed1` to `observed10` and `diff1` to `diff10`) are undocumented and mostly empty. Using undocumented columns without physical meaning leads to poor scientific integrity, so we strictly used verified sensor variables.

---

### Q6: How did you handle records with `capacity = 0`? Why didn't you impute them?
**Answer:**  
Out of 5.08 million rows, 494,235 rows (9.7%) have zero capacity. Calculating occupancy percentage `(occupied / capacity) * 100` would cause a **division-by-zero error**. These rows represent street sweeping, construction, or temporary parking suspensions. We **filtered these rows out** rather than imputing fake values, because inventing capacity numbers would falsify actual street geometry.

---

### Q7: What are lag features and why did you create them?
**Answer:**  
Lag features capture historical momentum. Since parking demand changes continuously, we created:
- **`occ_lag_15`**: Occupancy 15 minutes earlier (shift of 3 periods).
- **`occ_lag_30`**: Occupancy 30 minutes earlier (shift of 6 periods).
- **`occ_lag_60`**: Occupancy 60 minutes earlier (shift of 12 periods).  
These allow the model to learn the velocity and direction (filling up vs. emptying out) of parking demand.

---

### Q8: What is Data Leakage and how did you prevent it?
**Answer:**  
Data leakage occurs when information from the future or outside the training dataset is inadvertently used to train the model, resulting in unrealistically high training scores that fail in production. We prevented it by:
1. Calculating lags and targets **strictly within each segment** (preventing cross-street contamination).
2. Ensuring the future target (60 min ahead) is **never included in the feature matrix $X$**.
3. Using a **strict chronological train-validation-test split** (training on earlier dates, testing on later dates) rather than random splitting.

---

### Q9: Why did you use a chronological split instead of `train_test_split(shuffle=True)`?
**Answer:**  
Parking occupancy is a time series with strong temporal autocorrelation. If we use random shuffling, the model might train on 10:05 AM and test on 10:00 AM of the same day. The model would simply memorize adjacent time points, artificially inflating accuracy. A chronological split ensures the model truly learns to forecast unseen future days.

---

### Q10: Why did you implement 8 different classification algorithms?
**Answer:**  
To fulfill **Experiment 9 of our ML Lab syllabus** and follow the No-Free-Lunch theorem:
1. Logistic Regression (linear baseline)
2. Naive Bayes (probabilistic)
3. MLP Classifier (Artificial Neural Network)
4. Support Vector Machine (kernel margin separator)
5. K-Nearest Neighbors (instance-based)
6. Decision Tree (rule-based)
7. Random Forest (bagging ensemble)
8. AdaBoost (boosting ensemble)

---

### Q11: What is the "Persistence Baseline" and why is it important in parking?
**Answer:**  
The persistence baseline simply predicts that **the class 60 minutes from now will be the same as the current class** ($y_{t+60} = y_t$). Because parking occupancy drifts gradually, persistence is a very strong benchmark (scoring 0.740 Macro F1). Comparing ML models against persistence ensures our machine learning model is adding genuine predictive value beyond simple inertia.

---

### Q12: Which model performed the best and what were its scores?
**Answer:**  
**Random Forest Classifier** performed best:
- Validation Macro F1: **0.744** (vs. Persistence: 0.740)
- Held-out Test Accuracy: **74.8%** (0.748)
- Held-out Test Macro F1: **0.736** (vs. Persistence: 0.729)
- Recall on Full Class: **0.74**

---

### Q13: Why did Naive Bayes perform so poorly (~41.2% Macro F1)?
**Answer:**  
Naive Bayes relies on the strict assumption that all input features are **conditionally independent**. However, our lag features (`occ_lag_15`, `occ_lag_30`, `occ_lag_60`) are **strongly correlated** ($r > 0.85$). Because they violate the independence assumption, Naive Bayes severely multiplies redundant probabilities and misclassifies samples.

---

### Q14: Why do KNN, SVM, and Logistic Regression require feature scaling, while Decision Trees and Random Forests do not?
**Answer:**  
- **KNN, SVM, Logistic Regression, and MLP** rely on distance metrics (Euclidean distance) or gradient descent. If one feature has values from 0 to 100 (`occupancy_pct`) and another has values 0 to 1 (`is_weekend`), the larger scale feature dominates the calculations without `StandardScaler`.
- **Decision Trees and Random Forests** make axis-aligned split decisions based on ordering and thresholding ($X_j \le \text{threshold}$). Monotonic scaling does not change the ordering of values, so scaling has zero impact on tree splits.

---

### Q15: How does a Decision Tree decide where to split?
**Answer:**  
A Decision Tree evaluates all candidate split thresholds across features to find the split that maximizes the drop in impurity. In classification, it uses **Gini Impurity** or **Entropy (Information Gain)**:
$$\text{Gini} = 1 - \sum_{i=1}^{C} p_i^2$$
The split that produces the lowest weighted child Gini impurity is chosen.

---

### Q16: How does Random Forest improve upon a single Decision Tree?
**Answer:**  
A single decision tree often suffers from high variance (overfitting). Random Forest is an ensemble method that combines multiple trees using:
1. **Bootstrap Aggregating (Bagging):** Each tree is trained on a random sample of the training data with replacement.
2. **Feature Randomness:** At each split, only a random subset of features is evaluated.
Taking the majority vote across 100 trees reduces variance without increasing bias.

---

### Q17: What is Macro F1-Score and why is it preferred over Accuracy here?
**Answer:**  
In our dataset, the classes are imbalanced: Available is 41.1%, Nearly Full is 39.1%, and **Full is only 19.8%**. Standard accuracy treats all correct predictions equally. **Macro F1-Score** calculates the F1-score for each class independently and takes the unweighted arithmetic mean:
$$\text{Macro } F1 = \frac{F1_{\text{Available}} + F1_{\text{Nearly Full}} + F1_{\text{Full}}}{3}$$
This gives equal importance to the minority class (Full), ensuring the model is evaluated on all three categories.

---

### Q18: What is the most costly classification error in smart parking?
**Answer:**  
The most critical error is predicting **Available** when the parking segment is actually **Full**. A commuter travels to that block expecting empty spaces, only to find zero parking, worsening traffic jams and driver frustration. In contrast, predicting Nearly Full when Available is minor. Our Random Forest model minimized this critical error to **only 255 out of 7,191 test cases (< 3.5%)**.

---

### Q19: What is hyperparameter tuning and how did you do it?
**Answer:**  
Hyperparameters are configuration settings external to the model (like `max_depth` and `n_estimators`). We tuned them using `GridSearchCV` combined with `TimeSeriesSplit` (chronological cross-validation) so future data is never used to validate past folds. Tuning `max_depth=12` and `min_samples_leaf=2` improved tree stability and generalization.

---

### Q20: What does the Streamlit web application do?
**Answer:**  
`app.py` provides an interactive smart-city dashboard where users can:
1. Select any of the 420 parking block segments.
2. Choose a date and time.
3. Automatically load SFpark historical hourly averages or enter live sensor readings.
4. View real-time predictions for **Now, T+15, T+30, T+45, T+60, T+90, and T+120 minutes**.
5. Inspect color-coded metric cards (Green, Amber, Red), occupancy trend charts, and download a CSV forecast.

---

### Q21: What are the main limitations of your project?
**Answer:**  
1. **Geographical & Temporal Context:** The training data is from San Francisco in 2013 and has not yet been validated on Indian city roads or university campuses.
2. **Missing External Context:** The dataset lacks weather (rainy days), public holidays, and local sports/concert events.
3. **Small Segment Capacities:** The median segment capacity is only 8 bays; the arrival of just one car changes occupancy by 12.5%, making single-space changes noisy.

---

### Q22: Why did Random Forest only marginally beat the Persistence Baseline (0.736 vs 0.729)?
**Answer:**  
This is an **honest and realistic finding** in urban parking modeling. Street occupancy has strong physical inertia—an occupied car stays parked for an average of 45–90 minutes. However, during morning rush hours and evening office departures, parking demand experiences sharp non-linear phase transitions that persistence completely misses, but Random Forest captures through time-of-day and lag features.

---

### Q23: How would you extend this project in the future?
**Answer:**  
1. Connect to live IoT ultrasonic/magnetic ground sensors or AI camera feeds.
2. Integrate weather API data and city holiday calendars as exogenous features.
3. Explore deep learning sequence models like LSTMs or GRUs for multi-step trajectory forecasting.

---

### Q24: How does KNN classify a test sample?
**Answer:**  
KNN computes the Euclidean distance between the test sample and all training samples in feature space:
$$d(x, x') = \sqrt{\sum_{i=1}^{n} (x_i - x_i')^2}$$
It identifies the $k$ nearest neighbors (we used $k=7$) and assigns the majority class among them.

---

### Q25: How did you deploy and test the project?
**Answer:**  
The model and metadata were serialized using `joblib.dump()`. The Streamlit application was executed locally or via Google Colab and exposed using a tunneling proxy (`localtunnel` / `ngrok`) on port 8501, allowing cross-platform browser access on desktops and mobile devices.
