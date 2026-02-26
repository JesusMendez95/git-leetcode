from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path

from .algomap_scraper import build_catalog, load_catalog
from .documentation import write_docs, write_solution_file
from .leetcode_details import fetch_problem_details, problem_details_to_dict
from .models import Challenge
from .solver import can_solve, solve_challenge


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {"history": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _pick_daily_challenge(challenges: list[Challenge], run_date: date) -> Challenge:
    solvable = [c for c in challenges if can_solve(c)]
    if not solvable:
        raise RuntimeError("No hay retos con solver implementado.")
    days = (run_date - date(2024, 1, 1)).days
    return solvable[days % len(solvable)]


def _run_git_command(repo_dir: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def ensure_git_repo(repo_dir: Path, remote_url: str | None) -> None:
    git_dir = repo_dir / ".git"
    if not git_dir.exists():
        _run_git_command(repo_dir, ["init"])
    if remote_url:
        remotes = _run_git_command(repo_dir, ["remote"])
        if "origin" not in remotes.splitlines():
            _run_git_command(repo_dir, ["remote", "add", "origin", remote_url])


def publish_changes(repo_dir: Path, commit_message: str) -> None:
    target_branch = "develop"
    try:
        _run_git_command(repo_dir, ["checkout", target_branch])
    except RuntimeError:
        _run_git_command(repo_dir, ["checkout", "-b", target_branch])

    _run_git_command(repo_dir, ["add", "."])
    status = _run_git_command(repo_dir, ["status", "--porcelain"])
    if not status:
        return

    commit_name = os.getenv("GIT_COMMIT_NAME") or os.getenv("GITHUB_USERNAME")
    commit_email = os.getenv("GIT_COMMIT_EMAIL")
    if not commit_email and commit_name:
        commit_email = f"{commit_name}@users.noreply.github.com"

    commit_args = ["commit", "-m", commit_message]
    if commit_name and commit_email:
        commit_args = [
            "-c",
            f"user.name={commit_name}",
            "-c",
            f"user.email={commit_email}",
            *commit_args,
        ]
    _run_git_command(repo_dir, commit_args)

    remotes = _run_git_command(repo_dir, ["remote"])
    if "origin" not in remotes.splitlines():
        raise RuntimeError("No existe remote origin. Configuralo para hacer push.")

    _run_git_command(repo_dir, ["push", "-u", "origin", target_branch])


def run_daily_pipeline(
    repo_dir: Path,
    roadmap_url: str,
    run_date: date,
    skip_push: bool,
    remote_url: str | None,
    force_problem_id: int | None = None,
) -> dict:
    catalog_path = repo_dir / "data" / "algomap_challenges.json"
    state_path = repo_dir / "state" / "daily_state.json"

    if not catalog_path.exists():
        build_catalog(roadmap_url, catalog_path)

    challenges = load_catalog(catalog_path)
    challenge = (
        next((c for c in challenges if c.leetcode_id == force_problem_id), None)
        if force_problem_id
        else _pick_daily_challenge(challenges, run_date)
    )
    if challenge is None:
        raise RuntimeError(f"No se encontro el reto con ID {force_problem_id} en el catalogo.")

    result = solve_challenge(challenge)
    problem_details = fetch_problem_details(challenge.slug, challenge.title)
    solution_path = write_solution_file(repo_dir / "solutions", result)

    process_path = write_docs(
        base_docs_dir=repo_dir / "docs",
        result=result,
        problem_details=problem_details,
        run_date=run_date,
    )

    state = _load_state(state_path)
    entry = {
        "date": run_date.isoformat(),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "challenge": asdict(challenge),
        "problem_details": problem_details_to_dict(problem_details),
        "solution_path": str(solution_path.relative_to(repo_dir)),
        "documentation_path": str(process_path.relative_to(repo_dir)),
        "screenshot_path": None,
    }
    state["history"] = [h for h in state.get("history", []) if h.get("date") != run_date.isoformat()]
    state["history"].append(entry)
    _save_state(state_path, state)

    if not skip_push:
        ensure_git_repo(repo_dir, remote_url)
        commit_message = (
            f"feat: solve challenge {challenge.leetcode_id} "
            f"({challenge.slug}) for {run_date.isoformat()}"
        )
        publish_changes(repo_dir, commit_message)

    return entry
