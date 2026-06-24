"""Data ingestion helpers for SAFIR sensor datasets."""

from pathlib import Path
from typing import List, Dict
import pandas as pd


def load_sensor_csv(path: Path) -> List[Dict[str, float]]:
    """Load sensor readings from a CSV file into a list of records."""
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return [
        {
            "timestamp": row["timestamp"].isoformat(),
            "soil_moisture_pct": float(row["soil_moisture_pct"]),
            "solar_power_kw": float(row["solar_power_kw"]),
            "battery_level_pct": float(row["battery_level_pct"]),
            "groundwater_level_m": float(row["groundwater_level_m"]),
        }
        for _, row in df.iterrows()
    ]
