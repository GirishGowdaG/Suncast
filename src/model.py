"""
Solar PV forecasting model training and prediction.

Implements feature engineering, model training with Gradient Boosting,
and prediction utilities.

Author: Girish G
GitHub: https://github.com/GirishGowdaG/
"""

from pathlib import Path
from typing import Dict, Tuple

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Feature columns used for training
FEATURES = ["irradiance", "temp", "wind_speed", "hour", "dayofyear"]


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal features from timestamp column.

    Args:
        df: DataFrame with 'timestamp' column

    Returns:
        DataFrame with added 'hour' and 'dayofyear' columns
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["dayofyear"] = df["timestamp"].dt.dayofyear
    return df


def train(
    df: pd.DataFrame, out_path: str = "models/model.pkl"
) -> Tuple[GradientBoostingRegressor, float]:
    """
    Train Gradient Boosting model for solar PV prediction.

    Args:
        df: Training data with features and 'pv_output' target
        out_path: Path to save trained model

    Returns:
        Tuple of (trained_model, mae_on_test_set)
    """
    # Prepare features
    df = prepare(df)

    X = df[FEATURES]
    y = df["pv_output"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    # Train model
    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        verbose=0,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    # Save model
    out_path_obj = Path(out_path)
    out_path_obj.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)

    return model, mae


def predict_from_model(
    model: GradientBoostingRegressor, payload: Dict[str, any]
) -> float:
    """
    Make prediction from model using input payload.

    Args:
        model: Trained scikit-learn model
        payload: Dictionary with keys:
            - timestamp: ISO format datetime string
            - irradiance: float
            - temp: float
            - wind_speed: float

    Returns:
        Predicted PV output (kW) as float
    """
    # Parse timestamp
    ts = pd.to_datetime(payload["timestamp"])

    # Build feature DataFrame
    data = {
        "irradiance": [payload["irradiance"]],
        "temp": [payload["temp"]],
        "wind_speed": [payload["wind_speed"]],
        "hour": [ts.hour],
        "dayofyear": [ts.dayofyear],
    }

    df = pd.DataFrame(data)[FEATURES]

    # Predict
    prediction = model.predict(df)[0]

    return float(prediction)
