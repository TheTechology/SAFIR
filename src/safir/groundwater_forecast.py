"""Groundwater forecasting module for SAFIR."""

from typing import Any, Dict, Sequence
import numpy as np


class GroundwaterForecaster:
    """Simple scaffold for a groundwater forecasting model."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = None

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None:
        """Train a groundwater forecast model on historical features."""
        # TODO: replace with actual model training logic
        self.model = {
            "mean_target": np.mean(targets) if len(targets) else 0.0
        }

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict groundwater values for new feature rows."""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        return np.full(shape=(len(features),), fill_value=self.model["mean_target"])

    def evaluate(self, features: np.ndarray, targets: np.ndarray) -> float:
        """Evaluate forecast accuracy using mean absolute error."""
        predictions = self.predict(features)
        return float(np.mean(np.abs(predictions - targets)))
