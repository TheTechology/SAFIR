"""Reinforcement learning scheduler for SAFIR irrigation."""

from typing import Any, Dict
import numpy as np


class RLIrrigationScheduler:
    """Simple Q-learning scheduler scaffold."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.q_table = {}

    def _state_key(self, soil_moisture_pct: float, solar_kw: float) -> str:
        return f"{int(soil_moisture_pct)}:{int(solar_kw)}"

    def choose_action(self, soil_moisture_pct: float, solar_kw: float) -> str:
        key = self._state_key(soil_moisture_pct, solar_kw)
        return self.q_table.get(key, "wait")

    def update(self, soil_moisture_pct: float, solar_kw: float, action: str, reward: float) -> None:
        key = self._state_key(soil_moisture_pct, solar_kw)
        self.q_table[key] = action

    def reward(self, soil_moisture_pct: float, target_pct: float) -> float:
        return 1.0 - abs(soil_moisture_pct - target_pct) / 100.0
