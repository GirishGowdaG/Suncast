"""
Synthetic solar PV and weather data generator.

Generates realistic daily patterns for solar irradiance, temperature,
wind speed, and corresponding PV output.

Author: Girish G
GitHub: https://github.com/GirishGowdaG/
"""

import argparse
import math
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def sin_curve(hour: float, peak: float = 1000.0) -> float:
    """
    Generate sinusoidal irradiance pattern mimicking daily solar cycle.

    Args:
        hour: Hour of day (0-23)
        peak: Maximum irradiance value at solar noon

    Returns:
        Irradiance value (0 during night, sinusoidal during day)
    """
    if hour < 6 or hour > 18:
        return 0.0
    # Map 6-18 to 0-π for half sine wave
    angle = (hour - 6) / 12 * math.pi
    return peak * math.sin(angle)


def generate(days: int = 365, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic solar and weather data.

    Args:
        days: Number of days to generate
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns:
        - timestamp: datetime
        - irradiance: W/m² (0-1000)
        - temp: °C (10-35)
        - wind_speed: m/s (0-10)
        - pv_output: kW (derived from irradiance with noise)
    """
    np.random.seed(seed)

    # Generate hourly timestamps
    hours = days * 24
    start = pd.Timestamp("2024-01-01 00:00:00")
    timestamps = pd.date_range(start=start, periods=hours, freq="H")

    data = []
    for ts in timestamps:
        hour = ts.hour
        day_of_year = ts.dayofyear

        # Base irradiance with seasonal variation
        seasonal_factor = 1 + 0.2 * math.sin((day_of_year - 80) / 365 * 2 * math.pi)
        base_irr = sin_curve(hour, peak=1000) * seasonal_factor

        # Add realistic noise and clouds
        noise = np.random.normal(0, 50)
        cloud_factor = np.random.uniform(0.7, 1.0) if base_irr > 0 else 1.0
        irradiance = max(0, base_irr * cloud_factor + noise)

        # Temperature: warmer during day and summer
        temp_base = 20 + 10 * math.sin((day_of_year - 80) / 365 * 2 * math.pi)
        temp_daily = 5 * math.sin((hour - 6) / 12 * math.pi) if 6 <= hour <= 18 else -3
        temp = temp_base + temp_daily + np.random.normal(0, 2)

        # Wind speed: random with slight daily pattern
        wind_speed = abs(np.random.normal(3, 2))

        # PV output: proportional to irradiance with efficiency factor
        efficiency = 0.18  # ~18% panel efficiency
        pv_output = (irradiance * efficiency) + np.random.normal(0, 5)
        pv_output = max(0, pv_output)

        data.append(
            {
                "timestamp": ts,
                "irradiance": round(irradiance, 3),
                "temp": round(temp, 3),
                "wind_speed": round(wind_speed, 3),
                "pv_output": round(pv_output, 3),
            }
        )

    return pd.DataFrame(data)


def main():
    """CLI entry point for data generation."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic solar PV and weather data"
    )
    parser.add_argument(
        "--out",
        type=str,
        default="data/suncast.csv",
        help="Output CSV file path (default: data/suncast.csv)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of days to generate (default: 365)",
    )

    args = parser.parse_args()

    # Generate data
    df = generate(days=args.days, seed=42)

    # Create output directory if needed
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to CSV
    df.to_csv(out_path, index=False)

    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
