from __future__ import annotations

import re
from typing import Any

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from .models import ProblemDetails


LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _content_to_markdown(content_html: str) -> str:
    soup = BeautifulSoup(content_html, "html.parser")
    for sup in soup.find_all("sup"):
        sup.replace_with(f"^{sup.get_text(strip=True)}")
    lines: list[str] = []

    def handle_node(node: Any) -> None:
        if isinstance(node, NavigableString):
            return
        if not isinstance(node, Tag):
            return

        name = node.name.lower()
        text = _clean_text(node.get_text(" ", strip=True))

        if name in {"h1", "h2", "h3", "h4"} and text:
            level = min(int(name[1]), 4)
            lines.append(f"{'#' * level} {text}")
            lines.append("")
            return

        if name == "p" and text:
            lines.append(text)
            lines.append("")
            return

        if name == "ul":
            for li in node.find_all("li", recursive=False):
                item_text = _clean_text(li.get_text(" ", strip=True))
                if item_text:
                    lines.append(f"- {item_text}")
            lines.append("")
            return

        if name == "ol":
            index = 1
            for li in node.find_all("li", recursive=False):
                item_text = _clean_text(li.get_text(" ", strip=True))
                if item_text:
                    lines.append(f"{index}. {item_text}")
                    index += 1
            lines.append("")
            return

        if name == "pre":
            pre_text = node.get_text("\n", strip=True)
            if pre_text:
                lines.append("```text")
                lines.append(pre_text)
                lines.append("```")
                lines.append("")
            return

        for child in node.children:
            handle_node(child)

    for top in soup.contents:
        handle_node(top)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() or "Descripcion no disponible."


def _split_examples_and_constraints(description: str) -> tuple[list[str], list[str]]:
    examples: list[str] = []
    constraints: list[str] = []
    current: str | None = None

    for raw_line in description.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        low = line.lower()

        if low.startswith("example"):
            current = "examples"
            examples.append(line)
            continue

        if low.startswith("constraints"):
            current = "constraints"
            continue

        if current == "examples":
            examples.append(line)
        elif current == "constraints":
            normalized = line[2:].strip() if line.startswith("- ") else line
            constraints.append(normalized)

    return examples, constraints


def fetch_problem_details(slug: str, fallback_title: str) -> ProblemDetails:
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        content
      }
    }
    """
    response = requests.post(
        LEETCODE_GRAPHQL_URL,
        json={"query": query, "variables": {"titleSlug": slug}},
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    question = payload.get("data", {}).get("question")
    if not question:
        return ProblemDetails(
            title=fallback_title,
            description_markdown="Descripcion no disponible en este momento.",
            examples=[],
            constraints=[],
        )

    content_html = question.get("content") or ""
    description_markdown = _content_to_markdown(content_html)
    examples, constraints = _split_examples_and_constraints(description_markdown)

    return ProblemDetails(
        title=question.get("title") or fallback_title,
        description_markdown=description_markdown,
        examples=examples,
        constraints=constraints,
    )


def problem_details_to_dict(details: ProblemDetails) -> dict[str, Any]:
    return {
        "title": details.title,
        "description_markdown": details.description_markdown,
        "examples": details.examples,
        "constraints": details.constraints,
    }
