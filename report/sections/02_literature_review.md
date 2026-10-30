## 2. Literature Review

The escalation of vehicular traffic in metropolitan centers has elevated parking occupancy forecasting from an administrative convenience to a critical component of intelligent transportation systems (ITS) [1]. Empirical urban studies indicate that vehicles searching for parking constitute up to thirty percent of downtown congestion, amplifying vehicular emissions and commuter delays [2], [3]. Consequently, contemporary machine learning research has focused on predicting multi-facility parking occupancy from Internet of Things (IoT) sensor streams [4]. This literature landscape spans three dominant technical paradigms: deep sequential neural architectures, edge-oriented fog computing ensembles, and classical supervised decision trees [1]–[6].

### 2.1 Comparative Analysis of Recent Studies

Table 1 provides a systematic comparison of six recent, peer-reviewed investigations into smart parking availability prediction, summarizing their methodologies, target datasets, primary evaluation metrics, and practical operational tradeoffs.

**Table 1:** Comparative synthesis of recent peer-reviewed literature in smart parking occupancy prediction.

| Authors and Year | Proposed Methodology | Evaluated Dataset | Primary Reported Metric | Operational Tradeoff and Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Zhang et al. (2024)** [1] | MAT-LSTM (Multi-Head Attention + LSTM) vs. TCN | Multi-lot urban parking networks | Up to 48% accuracy gain over vanilla LSTM; MAE = 1.42 spaces | Substantial GPU resource demands; inference latency exceeding 100 ms hinders edge deployment. |
| **Enríquez et al. (2024)** [2] | AdaBoost classifier distributed across fog computing nodes | Urban mobility corridor telemetry | Classification Accuracy = 84.2%; Edge latency $< 15$ ms | Restricted to single-model boosting; lacks multi-lag temporal feature formulation. |
| **Dia et al. (2022)** [3] | Comparative evaluation: MLP, SVM, KNN, CART, and Random Forest | AIoT segment availability records | Random Forest Macro F1 = 0.812; MLP top neural model | Evaluated on static spatial segments without chronologically isolating test windows. |
| **Dahiya et al. (2024)** [4] | Supervised ensembles (Random Forest, SVM, Naive Bayes) | UCI Birmingham Parking benchmark | Precision = 87.4%; Recall = 85.9% across saturation bounds | Utilized non-chronological splitting, introducing potential temporal data leakage. |
| **Thai et al. (2022)** [5] | Long Short-Term Memory (LSTM) sequence network vs. AutoTS | UCI Birmingham Parking (30 facilities) | Outperformed baseline AutoTS in multi-step MSE | Continuous regression output does not align directly with municipal discrete signage categories. |
| **Gao et al. (2023)** [6] | Hybrid Discrete Wavelet Transform (DWT) + ConvGRU-BRC | Multi-lot European municipal parking feeds | Significant RMSE reduction over standard GRU and ARIMA | Multi-stage decomposition incurs severe computational overhead ($>45$ s training time). |

### 2.2 Critical Synthesis by Methodological Approach

A critical review of the literature reveals clear dichotomies between model complexity, predictive fidelity, and real-time operational feasibility:

#### Sequential Deep Learning and Hybrid Networks
Several authors argue that recurring daily travel cycles and parking accumulation demand recurrent neural networks capable of modeling temporal dynamics [1], [5], [6]. Zhang et al. [1] demonstrated that augmenting LSTM cells with multi-head self-attention mechanisms captures non-linear diurnal patterns across multi-block topologies, yielding a 48% accuracy boost over classical recurrent layers. Similarly, Gao et al. [6] combined wavelet noise filtering with convolutional gated recurrent units (ConvGRU) to resolve high-frequency sensor noise. However, as noted by Dia et al. [3], deep recurrent models introduce severe computational burdens: recurrent matrix multiplications and tensor reshaping incur high latency ($>100$ ms per inference), requiring dedicated GPU acceleration that municipal infrastructure and roadside edge units rarely support. Furthermore, deep regression formulations [5] predict raw continuous bay counts without mapping predictions to actionable operational capacity states.

#### Fog Computing and Edge Machine Learning
To circumvent network bottlenecks in centralized cloud architectures, researchers have explored lightweight classifiers deployed on localized fog gateways [2]. Enríquez et al. [2] implemented an AdaBoost pipeline on distributed fog nodes, achieving sub-15 millisecond response times and an 84.2% classification accuracy on 30-to-60-minute prediction horizons. Their findings confirm that ensemble classifiers offer exceptional inference speeds suitable for low-power edge nodes. Nonetheless, their architecture omitted multi-lag feature autoregression and did not benchmark modern gradient-boosted trees against classical bagging methods.

#### Supervised Ensemble Algorithms on Tabular Telemetry
In comparative benchmark settings, tree-based ensembles repeatedly demonstrate superior generalization on tabular IoT sensor records [3], [4]. Dahiya et al. [4] systematically evaluated six supervised algorithms on the Birmingham benchmark dataset, demonstrating that Random Forest significantly outperformed Support Vector Machines, K-Nearest Neighbors, and Naive Bayes in precision (87.4%) and recall (85.9%). The superior performance of decision tree ensembles stems from their inherent resistance to monotonic feature transformations, their capacity to model non-linear interactions between temporal indices and spatial facility IDs, and their robustness against sensor outliers [3].

### 2.3 Research Gaps and Project Formulation

Despite these advancements, existing literature exhibits three critical methodological limitations:
1. **Pervasive Temporal Data Leakage:** Most existing studies [3], [4] partition parking datasets using random cross-validation. In time-series telemetry recorded at 30-minute intervals, random sampling allows adjacent readings from the same afternoon into both training and evaluation subsets, yielding artificially inflated performance scores that fail when deployed on future calendar weeks.
2. **Neglect of Class Imbalance on Peak Saturation:** Standard accuracy metrics obscure severe minority-class failure [2], [4]. In real municipal datasets, lots operate at critical saturation ($\ge 80\%$ full) during only 14% to 18% of hours. Models evaluated solely on overall accuracy frequently fail to predict full facilities, precisely when driver warnings are most crucial.
3. **Absence of Actionable Consumer Decision Support:** Technical literature predominantly halts at statistical tables, offering neither plain-language driver guidance nor model-driven alternative routing when a target facility reaches capacity [1], [5], [6].

Our project directly addresses these deficiencies. We implement a strict **chronological $70/15/15$ split** (October 4 to November 27 for training; November 27 to December 8 for validation; December 8 to December 19 for held-out testing) to guarantee zero temporal data leakage. We engineer past-only autoregressive lag and rolling window features, apply cost-sensitive class balancing to ensure $>94\%$ recall on the saturated "Full" class, and deploy the resulting sub-millisecond Random Forest pipeline within an accessible, consumer-centric decision companion ("ParkWise").

