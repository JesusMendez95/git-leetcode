from __future__ import annotations

import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from .models import Challenge


_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


def _parse_slug(problem_url: str, fallback_url: str) -> str:
    m = re.search(r"/problems/([a-z0-9-]+)/?", problem_url)
    if m:
        return m.group(1)
    fallback = fallback_url.strip("/").split("/")[-1]
    return fallback or "unknown-problem"


def fetch_roadmap_html(roadmap_url: str) -> str:
    response = requests.get(
        roadmap_url,
        headers={"User-Agent": _UA},
        timeout=30,
    )
    response.raise_for_status()
    return response.text


def parse_challenges(html: str) -> list[Challenge]:
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.select("div.desktop-roadmap-view-section")
    by_id: dict[int, Challenge] = {}

    for section in sections:
        h2 = section.find("h2")
        if not h2:
            continue
        topic = h2.get_text(strip=True)
        rows = section.select("tbody tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 5:
                continue

            title_anchor = cells[0].find("a")
            if not title_anchor:
                continue

            title = title_anchor.get_text(strip=True)
            roadmap_url = title_anchor.get("href", "")
            if roadmap_url.startswith("/"):
                roadmap_url = f"https://algomap.io{roadmap_url}"

            difficulty = cells[1].get_text(strip=True)
            leet_anchor = cells[2].find("a")
            problem_url = leet_anchor.get("href", "") if leet_anchor else ""
            difficulty_score = cells[3].get_text(strip=True)
            status_cell = cells[4]
            status_id = status_cell.get("id", "")
            id_match = re.search(r"-(\d+)$", status_id)
            if not id_match:
                continue

            leetcode_id = int(id_match.group(1))
            slug = _parse_slug(problem_url, roadmap_url)

            by_id[leetcode_id] = Challenge(
                topic=topic,
                title=title,
                difficulty=difficulty,
                difficulty_score=difficulty_score,
                leetcode_id=leetcode_id,
                slug=slug,
                problem_url=problem_url,
                roadmap_url=roadmap_url,
            )

    return sorted(by_id.values(), key=lambda c: c.leetcode_id)


def build_catalog(roadmap_url: str, output_path: Path) -> list[Challenge]:
    html = fetch_roadmap_html(roadmap_url)
    challenges = parse_challenges(html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": roadmap_url,
        "count": len(challenges),
        "challenges": [c.to_dict() for c in challenges],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return challenges


def load_catalog(path: Path) -> list[Challenge]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Challenge(**item) for item in data["challenges"]]
