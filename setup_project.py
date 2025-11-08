#!/usr/bin/env python
"""Quick setup script to generate data and train model."""

import sys
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add src to path
sys.path.insert(0, "src")

from src import data_generator
from src import model

# Generate data
print("Generating synthetic data...")
df = data_generator.generate(days=365, seed=42)
os.makedirs("data", exist_ok=True)
df.to_csv("data/suncast.csv", index=False)
print(f"✓ Wrote {len(df)} rows to data/suncast.csv")

# Train model
print("\nTraining model...")
trained_model, mae = model.train(df, out_path="models/model.pkl")
print(f"✓ Trained model and saved to models/model.pkl. MAE: {mae:.3f}")

print("\n✅ Setup complete! You can now run:")
print("   python -m uvicorn src.api.main:app --reload")
