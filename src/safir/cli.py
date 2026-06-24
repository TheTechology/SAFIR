"""Command-line interface for SAFIR."""

import argparse
from pathlib import Path
from .data_ingestion import load_sensor_csv
from .server import run_api


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="safir",
        description="SAFIR AI irrigation monitoring and control service.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="Start the SAFIR API server")
    serve.add_argument("--host", default="127.0.0.1", help="Server host")
    serve.add_argument("--port", type=int, default=8000, help="Server port")

    ingest = subparsers.add_parser("ingest", help="Validate a sensor CSV file")
    ingest.add_argument("csv_path", type=str, help="Path to the sensor CSV file")

    args = parser.parse_args()

    if args.command == "serve":
        run_api(host=args.host, port=args.port)
    elif args.command == "ingest":
        path = Path(args.csv_path)
        if not path.exists():
            raise SystemExit(f"Error: file not found: {path}")
        records = load_sensor_csv(path)
        print(f"Loaded {len(records)} sensor records from {path}")
        print("Sample record:")
        print(records[0] if records else "No records available")
