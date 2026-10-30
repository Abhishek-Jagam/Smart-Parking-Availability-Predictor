# Project Implementation Progress & Verification Tracker

**Last Updated:** 2026-10-29  
**Status Overview:** Resumed session transitioning fully to the authentic Birmingham Car Park Occupancy dataset (`data/raw/dataset.csv`).

---

## Deliverables Status Matrix

| Component | Status | File-Path Evidence | Notes |
| :--- | :---: | :--- | :--- |
| **Raw Dataset** | **DONE** | `data/raw/dataset.csv` (1.4 MB, 35,717 rows) | UCI Birmingham dataset (30 car parks, Oct–Dec 2016, 08:00–16:30). |
| **Data Cleaning & Preprocessing** | **PARTIAL** | `src/preprocess.py` | Needs update to ingest Birmingham schema (`SystemCodeNumber`, `LastUpdated`, `Occupancy`, `Capacity`), engineer features, and perform chronological split. |
| **Model Training & Comparison** | **PARTIAL** | `src/train.py`, `results/metrics.csv` | Models previously trained on synthetic SFpark data; needs execution on real Birmingham processed splits. |
| **Saved Model & Metadata** | **PARTIAL** | `models/parking_model.joblib`, `models/model_metadata.json` | Requires updating with the retrained Birmingham Random Forest winner. |
| **300-DPI Publication Figures** | **PARTIAL** | `results/figures/` (4 figures exist) | Requires re-generation using real Birmingham test/val metrics. |
| **Jupyter / Colab Notebooks** | **PARTIAL** | `notebooks/01_data_cleaning_eda.ipynb`<br>`notebooks/02_model_training_comparison.ipynb`<br>`notebooks/03_best_model_export.ipynb` | Exist; need adaptation to Birmingham dataset and clean local re-execution via nbconvert. |
| **Frontend Dashboard (Streamlit)** | **PARTIAL** | `app.py`, `app/` (empty) | Needs migration into `app/main.py` with 5 screens: Predict, Status Board, Insights, Model Performance, About. Custom navy+teal styling, `.streamlit/config.toml`. |
| **Deployment Assets** | **MISSING** | `Dockerfile`, `.streamlit/config.toml` | Need creation for Streamlit Cloud and containerized fallback. |
| **Automated Test Suite** | **MISSING** | `tests/test_pipeline.py` | Need creation covering shapes, leak-free splits, and inference. |
| **Documentation & Viva Guide** | **PARTIAL** | `docs/DECISIONS.md`, `docs/AUDIT.md`, `docs/REQUIREMENTS_CHECKLIST.md` | Viva guide (`docs/VIVA_GUIDE.md`) and updated `README.md` need to be finalized with Birmingham dataset details. |
| **Academic Report** | **POSTPONED** | — | Explicitly out of scope per user instructions. |

---

## Immediate Next Steps
1. Document dataset and target decisions in `docs/DECISIONS.md`.
2. Update `src/preprocess.py` for Birmingham dataset: cleaning, target classification (`Available` vs `Nearly Full` / `Full`), feature engineering (lags, rolling, time features), and leak-free chronological split.
3. Update `src/train.py` to train all 8 syllabus models + XGBoost/LightGBM + Persistence Baseline on Birmingham data, save `results/metrics.csv`, figures, and model.
4. Update and execute all 3 notebooks in `notebooks/`.
5. Build `app/main.py`, `.streamlit/config.toml`, and `Dockerfile`.
6. Add `tests/test_pipeline.py` and run pytest.
7. Finalize `README.md` and `docs/VIVA_GUIDE.md`.

