"""Dashboard utilities for SAFIR open-data summaries."""

from typing import Any, Dict, Sequence


def summarize_sensor_data(records: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute a simple dashboard summary from sensor records."""
    if not records:
        return {"sensor_count": 0, "status": "waiting for data"}

    soil_moisture = [r["soil_moisture_pct"] for r in records]
    solar_power = [r["solar_power_kw"] for r in records]
    battery_level = [r["battery_level_pct"] for r in records]

    return {
        "sensor_count": len(records),
        "average_soil_moisture_pct": sum(soil_moisture) / len(soil_moisture),
        "average_solar_power_kw": sum(solar_power) / len(solar_power),
        "average_battery_level_pct": sum(battery_level) / len(battery_level),
        "latest_record": records[-1],
    }
