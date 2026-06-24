"""Realistic sensor data simulator for SAFIR — Vrancea, România, June 2026.

Models a 2 kW photovoltaic panel, 10 kWh battery, soil moisture with
evapotranspiration and automatic irrigation, and shallow groundwater depth.
All parameters are calibrated to Vrancea County conditions (lat ~45.8 N).
"""

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# ── PV panel ─────────────────────────────────────────────────────────────────
_PANEL_KW   = 2.0    # installed peak capacity
_SUNRISE_H  = 5.5    # 05:30 local (EEST, UTC+3)
_SUNSET_H   = 21.0   # 21:00 local
_SOLAR_NOON = 13.25  # solar noon for Vrancea in June
_SIGMA      = 3.8    # bell-curve half-width in hours

# ── Battery ───────────────────────────────────────────────────────────────────
_BATTERY_CAP_KWH = 10.0
_BASE_LOAD_KW    = 0.15   # always-on sensors + controller
_CHARGE_EFF      = 0.90   # charge/discharge round-trip efficiency

# ── Soil & irrigation ─────────────────────────────────────────────────────────
_IRR_TRIGGER = 32.0   # % — start pump when soil falls below this
_IRR_TARGET  = 56.0   # % — stop pump
_IRR_RATE    = 4.5    # % per hour while pump is active
_ET_DAY      = 0.18   # % per hour evapotranspiration 06–20 h
_ET_NIGHT    = 0.04   # % per hour 20–06 h

# ── Rainfall events (day_index: mm) ───────────────────────────────────────────
_RAIN_EVENTS: Dict[int, float] = {2: 11.0, 7: 7.5, 11: 19.0}


# ─────────────────────────────────────────────────────────────────────────────

def _solar_kw(hour: float, cloud_factor: float = 1.0) -> float:
    """Gaussian bell-curve PV output for Vrancea, June."""
    if hour <= _SUNRISE_H or hour >= _SUNSET_H:
        return 0.0
    raw = _PANEL_KW * math.exp(-0.5 * ((hour - _SOLAR_NOON) / _SIGMA) ** 2)
    return round(max(0.0, raw * cloud_factor), 3)


def _temperature_c(hour: float, day_index: int) -> float:
    """Sinusoidal air temperature: min ~18 °C at 06:00, max ~34 °C at 14:00."""
    t_min = 17.0 + (day_index % 7) * 0.3
    t_max = 33.5 - (day_index % 5) * 0.35
    if 6.0 <= hour <= 20.0:
        t = t_min + (t_max - t_min) * math.sin(math.pi * (hour - 6.0) / 14.0)
    else:
        t = t_min - 1.5
    return round(t, 1)


def generate(
    start: Optional[datetime] = None,
    days: int = 14,
    interval_hours: int = 1,
) -> List[Dict[str, Any]]:
    """
    Generate a realistic multi-day sensor data stream.

    Each record contains:
        timestamp, soil_moisture_pct, solar_power_kw, battery_level_pct,
        groundwater_level_m, temperature_c, rainfall_mm, irrigation_active.

    Args:
        start:          First timestamp (default: 2026-06-10 00:00).
        days:           Number of days to simulate.
        interval_hours: Time step in hours (1 = hourly).

    Returns:
        List of sensor record dicts ordered by time.
    """
    if start is None:
        start = datetime(2026, 6, 10, 0, 0, 0)

    records: List[Dict[str, Any]] = []
    soil       = 47.0
    battery    = 65.0
    gw         = 7.15   # groundwater depth in metres (deeper = higher value)
    irrigating = False

    for step in range(days * 24 // interval_hours):
        dt      = start + timedelta(hours=step * interval_hours)
        day_idx = (step * interval_hours) // 24
        hour    = dt.hour + dt.minute / 60.0

        cloud = 0.40 if day_idx in _RAIN_EVENTS else 1.0
        solar = _solar_kw(hour, cloud)
        temp  = _temperature_c(hour, day_idx)

        # Battery charge / discharge
        net_kw    = solar - _BASE_LOAD_KW
        delta_pct = (net_kw / _BATTERY_CAP_KWH) * 100.0 * interval_hours * _CHARGE_EFF
        battery   = max(5.0, min(100.0, battery + delta_pct))

        # Rainfall at 02:00 on rain days
        rainfall = 0.0
        if day_idx in _RAIN_EVENTS and dt.hour == 2 and dt.minute == 0:
            rainfall = _RAIN_EVENTS[day_idx]
            soil     = min(88.0, soil + rainfall * 0.75)
            gw       = max(4.0, gw - rainfall * 0.007)

        # Evapotranspiration
        et   = _ET_DAY if 6.0 <= hour <= 20.0 else _ET_NIGHT
        soil = max(8.0, soil - et * interval_hours)

        # Automatic irrigation cycle
        if soil <= _IRR_TRIGGER and not irrigating:
            irrigating = True
        if irrigating:
            soil = min(_IRR_TARGET, soil + _IRR_RATE * interval_hours)
            if soil >= _IRR_TARGET:
                irrigating = False

        # Groundwater: slow summer decline ~1.5 cm/day
        gw += 0.000625 * interval_hours

        records.append({
            "timestamp":           dt.isoformat(),
            "soil_moisture_pct":   round(soil, 2),
            "solar_power_kw":      solar,
            "battery_level_pct":   round(battery, 1),
            "groundwater_level_m": round(min(12.0, gw), 3),
            "temperature_c":       temp,
            "rainfall_mm":         round(rainfall, 1),
            "irrigation_active":   irrigating,
        })

    return records


def generate_24h(reference_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """Convenience wrapper: one clear sunny day, hourly, for chart previews."""
    if reference_date is None:
        reference_date = datetime(2026, 6, 15, 0, 0, 0)
    return generate(start=reference_date, days=1, interval_hours=1)
