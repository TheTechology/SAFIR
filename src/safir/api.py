"""FastAPI endpoints for SAFIR irrigation monitoring and data access."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

from . import simulator as _sim

app = FastAPI(
    title="SAFIR Irrigation Monitoring API",
    description="Open API for groundwater, soil moisture, solar irrigation, and scheduler data.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("static/index.html")


# ── Models ────────────────────────────────────────────────────────────────────

class SensorData(BaseModel):
    timestamp:           datetime
    soil_moisture_pct:   float
    solar_power_kw:      float
    battery_level_pct:   float
    groundwater_level_m: float
    temperature_c:       Optional[float] = None
    rainfall_mm:         Optional[float] = None
    irrigation_active:   Optional[bool]  = None


class ForecastResponse(BaseModel):
    timestamp:       datetime
    predicted_value: float
    metric:          str


sensor_store: List[SensorData] = []


# ── Core endpoints ────────────────────────────────────────────────────────────

@app.post("/sensor")
async def ingest_sensor_data(data: SensorData) -> Dict[str, Any]:
    sensor_store.append(data)
    return {"status": "stored", "count": len(sensor_store)}


@app.get("/sensor")
async def get_sensor_data(limit: int = Query(default=100, ge=1, le=10_000)) -> List[SensorData]:
    return sensor_store[-limit:]


@app.get("/forecast/groundwater")
async def groundwater_forecast() -> ForecastResponse:
    if not sensor_store:
        raise HTTPException(status_code=404, detail="No sensor data available")
    latest = sensor_store[-1]
    return ForecastResponse(
        timestamp=latest.timestamp,
        predicted_value=latest.groundwater_level_m,
        metric="groundwater_level_m",
    )


@app.get("/dashboard")
async def dashboard_summary() -> Dict[str, Any]:
    if not sensor_store:
        return {"sensor_count": 0, "status": "waiting for data"}
    n = len(sensor_store)
    return {
        "sensor_count":             n,
        "last_timestamp":           sensor_store[-1].timestamp,
        "average_soil_moisture_pct": round(sum(d.soil_moisture_pct for d in sensor_store) / n, 2),
        "average_solar_power_kw":    round(sum(d.solar_power_kw    for d in sensor_store) / n, 3),
        "average_battery_level_pct": round(sum(d.battery_level_pct for d in sensor_store) / n, 1),
        "average_temperature_c":     round(
            sum(d.temperature_c for d in sensor_store if d.temperature_c is not None)
            / max(1, sum(1 for d in sensor_store if d.temperature_c is not None)), 1
        ),
        "latest_groundwater_level_m": sensor_store[-1].groundwater_level_m,
        "irrigation_events": sum(
            1 for d in sensor_store if d.irrigation_active
        ),
    }


@app.get("/project/info")
async def project_info() -> Dict[str, Any]:
    return {
        "name":         "SAFIR",
        "title":        "Agricultură inteligentă bazată pe inteligență artificială și irigații pentru reziliență",
        "organization": "Asociația Grupul Verde",
        "region":       "România, Croația, Albania, Danemarca, Germania & Laos",
        "team_size":    55,
        "countries":    ["România (12)", "Croația (11)", "Albania (11)", "Danemarca (11)", "Germania (10)"],
        "age_range":    "16–27 ani",
        "description":  "Proiect de monitorizare AI a irigațiilor, creat cu 35 de tineri din Vrancea",
        "features": [
            "Prognoză apă subterană",
            "Model LSTM pentru umiditate sol",
            "Control solar pentru irigații",
            "Programator învățare prin consolidare",
            "API deschis și date publice",
        ],
        "version": "0.1.0",
    }


@app.get("/project/team")
async def team_info() -> Dict[str, Any]:
    return {
        "organization": "Asociația Grupul Verde",
        "members":      55,
        "countries":    ["România", "Croația", "Albania", "Danemarca", "Germania"],
        "age_range":    "16–27 ani",
        "region":       "România, Croația, Albania, Danemarca, Germania",
        "focus":        "Agricultură durabilă și adaptare climatică",
        "technologies": ["Python", "FastAPI", "TensorFlow", "LSTM", "AI/RL"],
    }


@app.get("/api/status")
async def api_status() -> Dict[str, Any]:
    return {
        "status":            "running",
        "timestamp":         datetime.now().isoformat(),
        "sensors_connected": len(sensor_store),
        "api_version":       "0.1.0",
        "endpoints": [
            {"path": "/sensor",                  "methods": ["GET", "POST"], "desc": "Sensor data ingestion"},
            {"path": "/dashboard",               "methods": ["GET"],         "desc": "Dashboard summary"},
            {"path": "/forecast/groundwater",    "methods": ["GET"],         "desc": "Groundwater forecast"},
            {"path": "/simulate/preview",        "methods": ["GET"],         "desc": "24 h realistic preview"},
            {"path": "/simulate/week",           "methods": ["GET"],         "desc": "14-day simulation data"},
            {"path": "/simulate/load",           "methods": ["POST"],        "desc": "Load simulation into store"},
            {"path": "/project/info",            "methods": ["GET"],         "desc": "Project information"},
            {"path": "/project/team",            "methods": ["GET"],         "desc": "Team information"},
        ],
    }


# ── Simulation endpoints ──────────────────────────────────────────────────────

@app.get("/simulate/preview")
async def simulate_preview() -> List[Dict[str, Any]]:
    """Return one sunny day of hourly data (24 records) without storing anything.
    Use this to populate charts without side effects."""
    return _sim.generate_24h()


@app.get("/simulate/week")
async def simulate_week(
    days: int = Query(default=14, ge=1, le=30),
    interval_hours: int = Query(default=1, ge=1, le=6),
) -> List[Dict[str, Any]]:
    """Return *days* days of simulated hourly sensor data without storing it.

    Query params:
    - days: 1–30 (default 14)
    - interval_hours: 1–6 (default 1)
    """
    return _sim.generate(days=days, interval_hours=interval_hours)


@app.post("/simulate/load")
async def simulate_load(
    days: int = Query(default=14, ge=1, le=30),
    interval_hours: int = Query(default=1, ge=1, le=6),
    clear: bool = Query(default=True),
) -> Dict[str, Any]:
    """Generate realistic simulation data and load it into the sensor store.

    Query params:
    - days: number of days to simulate (default 14)
    - interval_hours: step size in hours (default 1)
    - clear: whether to clear existing data first (default true)
    """
    global sensor_store
    if clear:
        sensor_store = []

    records = _sim.generate(days=days, interval_hours=interval_hours)
    for r in records:
        sensor_store.append(SensorData(**r))

    return {
        "status":   "loaded",
        "records":  len(records),
        "days":     days,
        "interval": f"{interval_hours}h",
        "store_total": len(sensor_store),
    }


@app.delete("/simulate/clear")
async def simulate_clear() -> Dict[str, Any]:
    """Clear all data from the sensor store."""
    global sensor_store
    count = len(sensor_store)
    sensor_store = []
    return {"status": "cleared", "removed": count}
