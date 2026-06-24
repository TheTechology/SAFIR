"""LSTM soil moisture modeling module for SAFIR."""

from typing import Any, Dict
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam


class SoilMoistureLSTM:
    """Scaffold for an LSTM-based soil moisture prediction model."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = None

    def build_model(self, input_shape: tuple) -> Sequential:
        """Build the LSTM model architecture."""
        model = Sequential([
            LSTM(32, activation="tanh", input_shape=input_shape),
            Dense(16, activation="relu"),
            Dense(1, activation="linear"),
        ])
        model.compile(optimizer=Adam(learning_rate=0.001), loss="mse")
        self.model = model
        return model

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 10, batch_size: int = 32) -> None:
        """Train the LSTM model."""
        if self.model is None:
            self.build_model(input_shape=(x_train.shape[1], x_train.shape[2]))
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

    def predict(self, x_input: np.ndarray) -> np.ndarray:
        """Predict soil moisture values."""
        if self.model is None:
            raise ValueError("Model has not been built or trained yet")
        return self.model.predict(x_input)
