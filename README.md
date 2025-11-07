# SunCast – Day-Ahead Solar Power Forecasting (Week 1)

A production-ready Python project that predicts next-day solar PV output using machine learning.

**Developer:** Girish G [<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" height="20">](https://github.com/GirishGowdaG/)

## Goal

Build a complete ML pipeline for solar forecasting including:
- Synthetic data generation with realistic weather patterns
- Gradient boosting regression model
- REST API for real-time predictions
- Automated testing and CI/CD

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python src/data_generator.py --out data/suncast.csv --days 365
```

### 3. Train Model

```bash
python src/train.py --data data/suncast.csv --out models/model.pkl
```

### 4. Run Web Application

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to: **http://localhost:8000**

### 5. Test Prediction (Web UI)

Use the interactive web interface to:
- Set date/time and weather conditions
- Use quick presets (Sunny Day, Cloudy, Night)
- Get instant predictions with visualizations

### 6. Test Prediction (API)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"timestamp\":\"2025-06-15T14:00:00\",\"irradiance\":850.5,\"temp\":28.3,\"wind_speed\":3.2}"
```

Expected response:
```json
{
  "prediction": 153.42
}
```

## Definition of Done

✅ Data generator creates realistic synthetic solar/weather data  
✅ Model trains with <10% MAE and saves to `models/model.pkl`  
✅ **Web application with interactive UI at http://localhost:8000**  
✅ API returns predictions via `/predict` endpoint  
✅ All tests pass (`pytest`)  
✅ CI pipeline validates code quality and tests  

## Directory Structure

```
suncast/
├─ README.md              # This file
├─ requirements.txt       # Python dependencies
├─ .gitignore            # Git ignore patterns
├─ LICENSE               # MIT License
├─ src/
│  ├─ data_generator.py  # Synthetic data generation
│  ├─ model.py           # ML model training & prediction
│  ├─ train.py           # CLI for model training
│  ├─ api/
│  │  └─ main.py         # FastAPI REST service
│  └─ web/
│     ├─ templates/
│     │  └─ index.html   # Web UI
│     └─ static/
│        ├─ css/
│        │  └─ style.css # Styles
│        └─ js/
│           └─ app.js    # Frontend logic
├─ tests/
│  ├─ test_model.py      # Core model tests
│  └─ test_model_additional.py  # Extended tests
└─ .github/
   └─ workflows/
      └─ ci.yml          # GitHub Actions CI

Generated at runtime:
├─ data/                 # CSV datasets
└─ models/               # Trained model artifacts
```

## Features

- **Interactive Web UI**: Beautiful, responsive interface for predictions
- **Synthetic Data**: Realistic solar irradiance patterns with day/night cycles
- **ML Model**: Gradient Boosting Regressor with temporal features
- **REST API**: FastAPI service with Pydantic validation
- **Quick Presets**: One-click weather scenarios (Sunny, Cloudy, Night)
- **Real-time Predictions**: Instant power output forecasts
- **Testing**: Pytest suite with 100% core coverage
- **CI/CD**: GitHub Actions for automated quality checks

## Next Steps (Future Weeks)

- 🐳 Dockerize application
- 📊 Add SHAP explainability
- 📈 Implement time-series forecasting (LSTM/Prophet)
- 🌍 Integrate real weather APIs
- 📱 Build web dashboard

## Author

**Girish G** [<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" height="20">](https://github.com/GirishGowdaG/)

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

**Built with Python 3.10+ | FastAPI | scikit-learn**  
**Created by Girish G** [<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="16" height="16">](https://github.com/GirishGowdaG/)
