#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from git_leetcode.pipeline import run_daily_pipeline


def _load_local_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _parse_date(raw: str | None) -> date:
    if not raw:
        return date.today()
    return date.fromisoformat(raw)


def main() -> None:
    _load_local_env()
    parser = argparse.ArgumentParser(description="Ejecuta reto diario + documentacion + git push.")
    parser.add_argument("--date", dest="run_date", help="Fecha ISO (YYYY-MM-DD)")
    parser.add_argument("--skip-push", action="store_true", help="No hace commit/push")
    parser.add_argument(
        "--allow-missing-screenshot",
        action="store_true",
        help="Permite generar artefactos sin screenshot",
    )
    parser.add_argument("--force-problem-id", type=int, help="Fuerza un reto por LeetCode ID")
    args = parser.parse_args()

    repo_dir = ROOT
    roadmap_url = os.getenv("ROADMAP_URL", "https://algomap.io/roadmap")
    remote_url = os.getenv("GIT_REMOTE_URL")

    entry = run_daily_pipeline(
        repo_dir=repo_dir,
        roadmap_url=roadmap_url,
        run_date=_parse_date(args.run_date),
        allow_missing_screenshot=args.allow_missing_screenshot,
        skip_push=args.skip_push,
        remote_url=remote_url,
        force_problem_id=args.force_problem_id,
    )

    print("Ejecucion completada")
    print(f"- Reto: {entry['challenge']['leetcode_id']} {entry['challenge']['title']}")
    print(f"- Solucion: {entry['solution_path']}")
    print(f"- Documentacion: {entry['documentation_path']}")
    print(f"- Screenshot: {entry['screenshot_path']}")


if __name__ == "__main__":
    main()
