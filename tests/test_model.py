"""
Core unit tests for solar PV forecasting model.

Tests data preparation, model training, and prediction pipeline.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.model import prepare, train, predict_from_model


@pytest.fixture
def sample_data():
    """Generate minimal synthetic dataset for testing (24 hours)."""
    timestamps = pd.date_range("2024-06-15", periods=24, freq="H")

    data = {
        "timestamp": timestamps,
        "irradiance": [
            0,
            0,
            0,
            0,
            0,
            0,
            100,
            300,
            500,
            700,
            850,
            950,
            1000,
            950,
            850,
            700,
            500,
            300,
            100,
            0,
            0,
            0,
            0,
            0,
        ],
        "temp": [
            15,
            14,
            14,
            13,
            13,
            14,
            16,
            19,
            22,
            25,
            27,
            29,
            30,
            29,
            28,
            26,
            23,
            20,
            18,
            16,
            15,
            15,
            14,
            14,
        ],
        "wind_speed": [
            2.1,
            1.8,
            1.5,
            1.3,
            1.2,
            1.4,
            2.0,
            2.5,
            3.1,
            3.5,
            3.8,
            4.0,
            3.9,
            3.7,
            3.4,
            3.0,
            2.7,
            2.3,
            2.0,
            1.8,
            1.7,
            1.9,
            2.0,
            2.1,
        ],
        "pv_output": [
            0,
            0,
            0,
            0,
            0,
            0,
            18,
            54,
            90,
            126,
            153,
            171,
            180,
            171,
            153,
            126,
            90,
            54,
            18,
            0,
            0,
            0,
            0,
            0,
        ],
    }

    return pd.DataFrame(data)


def test_prepare_adds_temporal_features(sample_data):
    """Test that prepare() adds hour and dayofyear columns."""
    df = prepare(sample_data)

    assert "hour" in df.columns
    assert "dayofyear" in df.columns
    assert df["hour"].min() == 0
    assert df["hour"].max() == 23
    assert df["dayofyear"].iloc[0] == 167  # June 15


def test_train_saves_model_and_returns_mae(sample_data, tmp_path):
    """Test that train() creates model file and returns valid MAE."""
    model_path = tmp_path / "model.pkl"

    model, mae = train(sample_data, out_path=str(model_path))

    assert model_path.exists()
    assert isinstance(mae, float)
    assert mae >= 0


def test_predict_from_model_returns_float(sample_data, tmp_path):
    """Test that prediction returns a float value."""
    model_path = tmp_path / "model.pkl"
    model, _ = train(sample_data, out_path=str(model_path))

    payload = {
        "timestamp": "2024-06-15T14:00:00",
        "irradiance": 850.5,
        "temp": 28.3,
        "wind_speed": 3.2,
    }

    prediction = predict_from_model(model, payload)

    assert isinstance(prediction, float)
    assert prediction >= 0
