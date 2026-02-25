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
    walkthrough_steps = [
        "Inicializa `best` con el primer valor para tener una referencia valida desde el inicio.",
        "Recorre los valores restantes y compara `abs(value)` contra `abs(best)`.",
        "Si `value` esta mas cerca de cero, actualiza `best`.",
        "Si hay empate de distancia (`abs(value) == abs(best)`), elige el mayor valor para priorizar el positivo.",
        "Al final retorna `best` como el numero mas cercano a cero segun la regla del problema.",
    ]
    why_it_works = (
        "El algoritmo mantiene un invariante: despues de procesar cada posicion, `best` es la mejor "
        "respuesta entre los elementos vistos. Como cada nuevo elemento compite contra ese mejor parcial, "
        "al terminar el recorrido se obtiene la solucion global correcta."
    )
    mermaid_diagram = """flowchart TD
    A[Inicio] --> B[best = nums[0]]
    B --> C{Quedan elementos?}
    C -->|No| H[Retornar best]
    C -->|Si| D[Tomar value]
    D --> E{abs(value) < abs(best)?}
    E -->|Si| F[best = value]
    E -->|No| G{abs(value) == abs(best) y value > best?}
    G -->|Si| F
    G -->|No| I[Conservar best]
    F --> C
    I --> C"""
    return SolveResult(
        challenge=challenge,
        code=code,
        language="python",
        explanation=explanation,
        complexity=complexity,
        walkthrough_steps=walkthrough_steps,
        why_it_works=why_it_works,
        mermaid_diagram=mermaid_diagram,
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
