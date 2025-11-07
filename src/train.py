"""
CLI script for training the solar PV forecasting model.

Loads CSV data, trains model, and saves to disk.

Author: Girish G
GitHub: https://github.com/GirishGowdaG/
"""

import argparse
from pathlib import Path

import pandas as pd

from model import train


def main():
    """CLI entry point for model training."""
    parser = argparse.ArgumentParser(description="Train solar PV forecasting model")
    parser.add_argument(
        "--data",
        type=str,
        default="data/suncast.csv",
        help="Path to training data CSV (default: data/suncast.csv)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="models/model.pkl",
        help="Output path for trained model (default: models/model.pkl)",
    )

    args = parser.parse_args()

    # Ensure models directory exists
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(args.data)

    # Train model
    model, mae = train(df, out_path=args.out)

    print(f"Trained model and saved to {args.out}. MAE: {mae:.3f}")


if __name__ == "__main__":
    main()
