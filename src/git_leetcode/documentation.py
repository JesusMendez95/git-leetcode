from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import SolveResult


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
    run_date: date,
    screenshot_path: Path | None,
) -> tuple[Path, Path]:
    target_dir = _challenge_dir(base_docs_dir, result)
    screenshots_dir = target_dir / "screenshots"
    target_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    screenshot_block = "Pendiente de adjuntar screenshot de envio exitoso."
    if screenshot_path and screenshot_path.exists():
        rel = screenshot_path.relative_to(target_dir)
        screenshot_block = f"![Envio exitoso]({rel.as_posix()})"

    readme = f"""# {result.challenge.title}

- Fecha: {run_date.isoformat()}
- Topic: {result.challenge.topic}
- Dificultad: {result.challenge.difficulty}
- LeetCode ID: {result.challenge.leetcode_id}
- Problema: {result.challenge.problem_url}
- Referencia en AlgoMap: {result.challenge.roadmap_url}

## Solucion ({result.language})

Archivo: `solutions/{result.language}/{result.challenge.leetcode_id}-{result.challenge.slug}.py`

## Evidencia

{screenshot_block}
"""

    process = f"""# Proceso de resolucion - {result.challenge.title}

## Enfoque

{result.explanation}

## Complejidad

{result.complexity}

## Validacion recomendada

1. Ejecutar casos simples (positivos, negativos, empate de valor absoluto).
2. Verificar que, en empate, se elige el numero positivo.
3. Confirmar envio exitoso en LeetCode y adjuntar screenshot en `docs/{result.challenge.leetcode_id}-{result.challenge.slug}/screenshots/`.
"""

    readme_path = target_dir / "README.md"
    process_path = target_dir / "process.md"
    readme_path.write_text(readme, encoding="utf-8")
    process_path.write_text(process, encoding="utf-8")
    return readme_path, process_path
