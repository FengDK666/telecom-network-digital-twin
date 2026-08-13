"""Command-line entry points."""

from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

from telecom_twin.experiment import run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic telecom network digital twin")
    subparsers = parser.add_subparsers(dest="command", required=True)
    experiment = subparsers.add_parser("experiment")
    experiment.add_argument("--output-dir", type=Path, default=Path("results"))
    serve = subparsers.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command == "experiment":
        for name, path in run_experiment(args.output_dir).items():
            print(f"{name}: {path}")
        return
    uvicorn.run("telecom_twin.api:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
