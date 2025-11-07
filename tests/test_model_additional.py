"""
Additional unit tests for extended model validation.

Tests with multi-day datasets and edge cases.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.model import train, predict_from_model


@pytest.fixture
def two_day_data():
    """Generate 48-hour synthetic dataset with realistic PV output."""
    timestamps = pd.date_range("2024-07-20", periods=48, freq="H")

    # Two days of hourly data
    irradiance_pattern = [0, 0, 0, 0, 0, 0, 150, 350, 550, 750, 900, 980,
                          1000, 980, 900, 750, 550, 350, 150, 0, 0, 0, 0, 0] * 2

    temp_pattern = [16, 15, 15, 14, 14, 15, 17, 20, 23, 26, 28, 30,
                    31, 30, 29, 27, 24, 21, 19, 17, 16, 16, 15, 15] * 2

    wind_pattern = [2.0, 1.7, 1.5, 1.3, 1.2, 1.5, 2.2, 2.8, 3.3, 3.7, 4.0, 4.2,
                    4.1, 3.9, 3.6, 3.2, 2.9, 2.5, 2.1, 1.9, 1.8, 1.9, 2.0, 2.1] * 2

    # PV output = irradiance × 0.18 (18% efficiency)
    pv_output = [irr * 0.18 for irr in irradiance_pattern]

    data = {
        "timestamp": timestamps,
        "irradiance": irradiance_pattern,
        "temp": temp_pattern,
        "wind_speed": wind_pattern,
        "pv_output": pv_output,
    }

    return pd.DataFrame(data)


def test_train_with_two_days(two_day_data, tmp_path):
    """Test model training with 48-hour dataset."""
    model_path = tmp_path / "model2.pkl"

    model, mae = train(two_day_data, out_path=str(model_path))

    assert model_path.exists()
    assert isinstance(mae, float)
    assert mae >= 0
    # MAE should be reasonable for this simple dataset
    assert mae < 50


def test_predict_afternoon_high_irradiance(two_day_data, tmp_path):
    """Test prediction for high solar irradiance conditions."""
    model_path = tmp_path / "model2.pkl"
    model, _ = train(two_day_data, out_path=str(model_path))

    payload = {
        "timestamp": "2024-07-20T13:00:00",
        "irradiance": 980.0,
        "temp": 30.0,
        "wind_speed": 4.2,
    }

    prediction = predict_from_model(model, payload)

    assert isinstance(prediction, float)
    assert prediction > 0
    # Should predict significant output for high irradiance
    assert prediction > 100


def test_predict_night_zero_irradiance(two_day_data, tmp_path):
    """Test prediction for nighttime conditions."""
    model_path = tmp_path / "model2.pkl"
    model, _ = train(two_day_data, out_path=str(model_path))

    payload = {
        "timestamp": "2024-07-20T02:00:00",
        "irradiance": 0.0,
        "temp": 15.0,
        "wind_speed": 1.5,
    }

    prediction = predict_from_model(model, payload)

    assert isinstance(prediction, float)
    # Should predict near-zero output at night
    assert prediction < 10
