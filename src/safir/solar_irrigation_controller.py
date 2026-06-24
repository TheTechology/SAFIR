"""Solar-powered irrigation controller logic for SAFIR."""

from typing import Dict, Any


class SolarIrrigationController:
    """Controller for managing irrigation based on solar power and water availability."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.state = {
            "last_irrigation": None,
            "pump_active": False,
        }

    def can_irrigate(self, solar_power_kw: float, battery_level_pct: float) -> bool:
        """Decide whether irrigation can run based on solar conditions."""
        min_power = self.config.get("min_solar_power_kw", 0.5)
        min_battery = self.config.get("min_battery_pct", 30.0)
        return solar_power_kw >= min_power or battery_level_pct >= min_battery

    def start_irrigation(self) -> None:
        self.state["pump_active"] = True

    def stop_irrigation(self) -> None:
        self.state["pump_active"] = False

    def schedule_irrigation(self, soil_moisture_pct: float, threshold_pct: float) -> bool:
        """Schedule irrigation when soil moisture is below threshold."""
        if soil_moisture_pct < threshold_pct:
            self.start_irrigation()
            return True
        self.stop_irrigation()
        return False
