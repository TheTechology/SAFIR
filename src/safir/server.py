"""Server launch helpers for SAFIR."""

import uvicorn
from .api import app


def run_api(host: str = "127.0.0.1", port: int = 8000) -> None:
    uvicorn.run(app, host=host, port=port)
