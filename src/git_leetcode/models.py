from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Challenge:
    topic: str
    title: str
    difficulty: str
    difficulty_score: str
    leetcode_id: int
    slug: str
    problem_url: str
    roadmap_url: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SolveResult:
    challenge: Challenge
    code: str
    language: str
    explanation: str
    complexity: str
    walkthrough_steps: list[str]
    why_it_works: str
    mermaid_diagram: str


@dataclass(slots=True)
class ProblemDetails:
    title: str
    description_markdown: str
    examples: list[str]
    constraints: list[str]
