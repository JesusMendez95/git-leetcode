#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from git_leetcode.algomap_scraper import build_catalog


def main() -> None:
    repo_dir = ROOT
    catalog_path = repo_dir / "data" / "algomap_challenges.json"
    challenges = build_catalog("https://algomap.io/roadmap", catalog_path)
    print(f"Catalogo generado: {catalog_path}")
    print(f"Retos extraidos: {len(challenges)}")


if __name__ == "__main__":
    main()
