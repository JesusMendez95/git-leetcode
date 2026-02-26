from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import ProblemDetails, SolveResult


def _challenge_dir(base_docs_dir: Path, result: SolveResult) -> Path:
    slug = f"{result.challenge.leetcode_id}-{result.challenge.slug}"
    return base_docs_dir / slug


def write_solution_file(base_solutions_dir: Path, result: SolveResult) -> Path:
    filename = f"{result.challenge.leetcode_id}-{result.challenge.slug}.py"
    out_path = base_solutions_dir / result.language / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.code, encoding="utf-8")
    return out_path


def write_docs(
    base_docs_dir: Path,
    result: SolveResult,
    problem_details: ProblemDetails,
    run_date: date,
) -> Path:
    target_dir = _challenge_dir(base_docs_dir, result)
    target_dir.mkdir(parents=True, exist_ok=True)

    walkthrough_block = "\n".join(
        f"{idx}. {step}" for idx, step in enumerate(result.walkthrough_steps, start=1)
    )

    process = (
        f"# {result.challenge.title}\n\n"
        f"- Fecha: {run_date.isoformat()}\n"
        f"- Topic: {result.challenge.topic}\n"
        f"- Dificultad: {result.challenge.difficulty}\n"
        f"- LeetCode ID: {result.challenge.leetcode_id}\n"
        f"- Problema: {result.challenge.problem_url}\n"
        f"- Referencia en AlgoMap: {result.challenge.roadmap_url}\n\n"
        f"## Solucion ({result.language})\n\n"
        f"Archivo: `solutions/{result.language}/{result.challenge.leetcode_id}-{result.challenge.slug}.py`\n\n"
        "### Codigo\n\n"
        f"```{result.language}\n"
        f"{result.code.rstrip()}\n"
        "```\n\n"
        "## Descripcion del problema (LeetCode)\n\n"
        f"{problem_details.description_markdown}\n\n"
        "## Enfoque\n\n"
        f"{result.explanation}\n\n"
        "## Diagrama del algoritmo\n\n"
        "```mermaid\n"
        f"{result.mermaid_diagram}\n"
        "```\n\n"
        "## Desglose paso a paso del codigo\n\n"
        f"{walkthrough_block}\n\n"
        "## Por que funciona\n\n"
        f"{result.why_it_works}\n\n"
        "## Complejidad\n\n"
        f"{result.complexity}\n\n"
        "## Evidencia\n\n"
        "No aplica en este flujo automatico.\n"
    )

    process_path = target_dir / "process.md"
    process_path.write_text(process, encoding="utf-8")
    return process_path
