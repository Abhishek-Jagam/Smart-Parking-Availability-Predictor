# Existing Codebase Audit & Gap Analysis

**Date:** 2026-10-29  
**Auditor:** Senior ML Engineer  
**Project:** Smart Parking Availability Predictor (University ML Lab Mini Project - 15 Marks)

---

## 1. Inventory of Pre-existing Artifacts

Before this refactoring, the repository contained the following assets:
1. `app.py`: A single-file Streamlit application (~490 lines) with hardcoded segment definitions, visual styling, and placeholder rule-based heuristics if no model was present.
2. `notebooks/Smart_Parking_Predictor.ipynb` & `Smart_Parking_Predictor_Colab.py`: Prototype scripts outlining a 10-cell workflow with markdown explanations.
3. `reports/Smart_Parking_Project_Report.md` & `reports/Viva_Questions_and_Answers.md`: Markdown drafts of report content and viva questions.
4. `requirements.txt`: Minimal dependencies list.
5. `docs/`: Assignment instructions (`Mini Project Intsructions.pdf`, `ml guidelines.txt`, `Screenshot 2026-10-29 204952.png`).

---

## 2. Gap Analysis Against 15-Mark Rubric

| Component | Rubric Requirement | Existing Repo State | Status & Required Enhancements |
|:---|:---|:---|:---|
| **Data Cleaning & Splitting (3 Marks)** | Semicolon delimiter parsing, 0-capacity filtering, segment lag engineering ($t-15m, t-30m, t-60m$), chronological split ($70/15/15$), class distributions before/after, EDA figures. | Raw `data.csv` was missing from git. Notebook contained synthetic generation fallback logic. No modular `src/` scripts existed. | **Gap identified:** Create `src/download_data.py` and `src/preprocess.py` to automate data ingestion and leak-free splitting. Save raw and processed sets in `data/`. |
| **Model Comparison & Analytics (4 Marks)** | Compare all 8 syllabus models (LogReg, NB, ANN/MLP, SVM, KNN, Decision Tree, Random Forest, AdaBoost) + modern baselines (XGBoost/LightGBM). Accuracy, Precision, Recall, Macro F1, ROC-AUC, latency, confusion matrices, 300 DPI figures, serialized `model.joblib` and `metadata.json`. | Notebook had basic comparisons in markdown, but no stored `results/metrics.csv`, no 300 DPI figure outputs in `results/figures/`, and no saved serialized `.joblib` model file in `models/`. | **Gap identified:** Build `src/train.py` to systematically train, evaluate, and benchmark all 10 algorithms; export complete `metrics.csv`, generate 4 publication figures at 300 DPI, and serialize the best model + metadata. |
| **UI Deployment & Accessibility (4 Marks)** | Professional navy/teal city app, Streamlit, screens (Predict, Map, Insights, Model Performance, About), responsive mobile/desktop, input validation, friendly errors, Dockerfile. | Root `app.py` had good styling ideas but lacked a pydeck map, modular screen structure, and deployment configuration. | **Gap identified:** Refactor into `app/main.py` with custom theme in `.streamlit/config.toml`, integrate pydeck map, and create Dockerfile fallback. |
| **Code Quality & Repo (4 Marks)** | Modular structure (`src/`, `app/`, `notebooks/`, `tests/`), pytest tests, docstrings, type hints, professional README with pipeline diagram, Git instructions. | Monolithic files in root, no `src/` modules, no `tests/` directory, no unit tests. | **Gap identified:** Build modular packages in `src/`, add `tests/test_pipeline.py` with pytest verification, create comprehensive README. |
| **Report & Submission (Included in 4 Marks)** | Max 10-page report in DOCX and PDF, 5 verified recent papers (2022–2025) with DOIs, clean tables/figures, UI screenshots. | Only a markdown report existed; no generated `.docx` or `.pdf` matching the university format. | **Gap identified:** Verify 5 recent papers with Crossref DOIs, document in `docs/LITERATURE_LOG.md`, and generate professional `.docx` and `.pdf` reports. |

---

## 3. Remediation & Action Plan

1. **Phase 1: Ingestion & Preprocessing**  
   Implement `src/download_data.py` and `src/preprocess.py`. Generate `data/raw/` and `data/processed/` splits.
2. **Phase 2: Training Pipeline & Evaluation**  
   Implement `src/train.py`. Train all 10 models + baseline, generate `results/metrics.csv`, save 300 DPI figures to `results/figures/`, and save `models/parking_model.joblib` + `models/metadata.json`.
3. **Phase 3: Standard Colab Notebooks**  
   Create clean, top-to-bottom runnable `.ipynb` files in `notebooks/` (`01_data_cleaning_eda.ipynb`, `02_model_training_comparison.ipynb`, `03_best_model_export.ipynb`).
4. **Phase 4: Modern City UI**  
   Implement `app/main.py` with 5 screens and navy-teal theme.
5. **Phase 5: Automated Testing & Verification**  
   Implement `tests/test_pipeline.py` and run pytest.
6. **Phase 6: Academic Report & Viva Documentation**  
   Compile report into `.docx` and `.pdf` formats, and generate `docs/VIVA_GUIDE.md`.

