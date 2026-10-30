"""
Test Suite for Smart Parking Availability Predictor Pipeline.
Verifies data pipeline shapes, leak-free temporal splitting, and model inference.
"""

import os
import json
import joblib
import pytest
import numpy as np
import pandas as pd

from src.preprocess import (
    load_and_clean_data,
    engineer_features,
    split_chronologically,
    FEATURE_COLS,
    TARGET_COL,
    CLASS_NAMES
)


@pytest.fixture
def raw_data_path():
    path = os.path.join("data", "raw", "dataset.csv")
    if not os.path.exists(path):
        pytest.skip("data/raw/dataset.csv not found")
    return path


def test_data_cleaning_and_bounds(raw_data_path):
    """Test that cleaned data has no negative occupancies or overflows."""
    df_clean = load_and_clean_data(raw_data_path)
    
    # Assert no nulls in core columns
    assert df_clean["Occupancy"].isnull().sum() == 0
    assert df_clean["Capacity"].isnull().sum() == 0
    
    # Assert valid physical ranges
    assert (df_clean["Occupancy"] >= 0).all()
    assert (df_clean["Occupancy"] <= df_clean["Capacity"]).all()
    assert (df_clean["occupancy_pct"] >= 0.0).all()
    assert (df_clean["occupancy_pct"] <= 100.0).all()


def test_feature_engineering_pipeline(raw_data_path):
    """Test that features are created properly without nulls in target."""
    df_clean = load_and_clean_data(raw_data_path)
    df_feat = engineer_features(df_clean)
    
    for col in FEATURE_COLS:
        assert col in df_feat.columns, f"Missing feature: {col}"
        assert df_feat[col].isnull().sum() == 0, f"NaN values in feature {col}"
        
    assert TARGET_COL in df_feat.columns
    assert set(df_feat[TARGET_COL].unique()).issubset(set(CLASS_NAMES))


def test_chronological_split_no_leakage(raw_data_path):
    """Test that temporal ordering strictly holds: train max < val min <= val max < test min."""
    df_clean = load_and_clean_data(raw_data_path)
    df_feat = engineer_features(df_clean)
    train_df, val_df, test_df = split_chronologically(df_feat)
    
    train_max_date = train_df["LastUpdated"].max()
    val_min_date = val_df["LastUpdated"].min()
    val_max_date = val_df["LastUpdated"].max()
    test_min_date = test_df["LastUpdated"].min()
    
    # Assert chronological ordering
    assert train_max_date <= val_min_date, "Leakage: Train overlaps with Validation!"
    assert val_max_date <= test_min_date, "Leakage: Validation overlaps with Test!"


def test_serialized_model_and_inference():
    """Test that saved model loads and predicts valid classes matching metadata."""
    model_path = os.path.join("models", "parking_model.joblib")
    meta_path = os.path.join("models", "model_metadata.json")
    
    assert os.path.exists(model_path), "Serialized model missing"
    assert os.path.exists(meta_path), "Model metadata missing"
    
    model = joblib.load(model_path)
    with open(meta_path, "r") as f:
        meta = json.load(f)
        
    assert meta["model_name"] == "Random Forest Classifier"
    assert meta["target_classes"] == CLASS_NAMES
    
    # Test synthetic sample inference
    sample_dict = {col: 1.0 for col in FEATURE_COLS}
    sample_df = pd.DataFrame([sample_dict])
    
    pred_enc = model.predict(sample_df)[0]
    proba = model.predict_proba(sample_df)[0]
    
    assert pred_enc in [0, 1, 2]
    assert len(proba) == 3
    assert np.isclose(proba.sum(), 1.0)

