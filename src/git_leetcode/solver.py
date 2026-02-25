from __future__ import annotations

from .models import Challenge, SolveResult


def _solve_2239(challenge: Challenge) -> SolveResult:
    code = '''from typing import List


class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        best = nums[0]
        for value in nums[1:]:
            if abs(value) < abs(best):
                best = value
            elif abs(value) == abs(best) and value > best:
                best = value
        return best
'''
    explanation = (
        "Recorre el arreglo una vez y conserva el numero con menor valor absoluto. "
        "En empate por valor absoluto, se elige el mayor numero para privilegiar el positivo."
    )
    complexity = "Tiempo O(n), espacio O(1)."
    return SolveResult(
        challenge=challenge,
        code=code,
        language="python",
        explanation=explanation,
        complexity=complexity,
    )


SOLVER_REGISTRY = {
    2239: _solve_2239,
}


def can_solve(challenge: Challenge) -> bool:
    return challenge.leetcode_id in SOLVER_REGISTRY


def solve_challenge(challenge: Challenge) -> SolveResult:
    solver = SOLVER_REGISTRY.get(challenge.leetcode_id)
    if not solver:
        raise ValueError(
            f"No hay solucion automatica para el reto {challenge.leetcode_id} ({challenge.slug})."
        )
    return solver(challenge)
