"""
FastAPI REST service for solar PV forecasting.

Provides /predict endpoint for real-time power output predictions.

Author: Girish G
GitHub: https://github.com/GirishGowdaG/
"""

import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..model import predict_from_model

# Pydantic models for request/response validation


class PredictRequest(BaseModel):
    """Request schema for prediction endpoint."""

    timestamp: str
    irradiance: float
    temp: float
    wind_speed: float


class PredictResponse(BaseModel):
    """Response schema for prediction endpoint."""

    prediction: float


# Initialize FastAPI app
app = FastAPI(
    title="SunCast API",
    description="Day-ahead solar PV power forecasting service",
    version="1.0.0",
    contact={
        "name": "Girish G",
        "url": "https://github.com/GirishGowdaG/",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Setup static files and templates
CURRENT_DIR = Path(__file__).parent
WEB_DIR = CURRENT_DIR.parent / "web"
app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))

# Global model placeholder
model = None


@app.on_event("startup")
async def load_model():
    """
    Load trained model on application startup.

    Reads model path from SUNC_MODEL environment variable
    or defaults to models/model.pkl.

    Raises:
        FileNotFoundError: If model file does not exist
    """
    global model

    model_path = os.getenv("SUNC_MODEL", "models/model.pkl")
    model_file = Path(model_path)

    if not model_file.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Please train model first using: python src/train.py"
        )

    model = joblib.load(model_file)
    print(f"✓ Loaded model from {model_path}")


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    """
    Predict solar PV output for given weather conditions.

    Args:
        request: PredictRequest with timestamp and weather features

    Returns:
        PredictResponse with predicted power output (kW)

    Raises:
        HTTPException: If model not loaded or prediction fails
    """
    if model is None:
        raise HTTPException(
            status_code=503, detail="Model not loaded. Check server startup logs."
        )

    try:
        payload = request.dict()
        prediction = predict_from_model(model, payload)

        return PredictResponse(prediction=prediction)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve web application."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "service": "SunCast API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "developer": "Girish G",
        "github": "https://github.com/GirishGowdaG/",
    }
