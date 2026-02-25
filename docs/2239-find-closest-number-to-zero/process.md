# Find Closest Number to Zero

- Fecha: 2026-02-25
- Topic: Arrays & Strings
- Dificultad: Easy
- LeetCode ID: 2239
- Problema: https://leetcode.com/problems/find-closest-number-to-zero/description/
- Referencia en AlgoMap: https://algomap.io/problems/find-closest-number-to-zero

## Solucion (python)

Archivo: `solutions/python/2239-find-closest-number-to-zero.py`

### Codigo

```python
from typing import List


class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        best = nums[0]
        for value in nums[1:]:
            if abs(value) < abs(best):
                best = value
            elif abs(value) == abs(best) and value > best:
                best = value
        return best
```

## Descripcion del problema (LeetCode)

Given an integer array nums of size n , return the number with the value closest to 0 in nums . If there are multiple answers, return the number with the largest value .

Example 1:

```text
Input:
nums = [-4,-2,1,4,8]
Output:
1
Explanation:
The distance from -4 to 0 is |-4| = 4.
The distance from -2 to 0 is |-2| = 2.
The distance from 1 to 0 is |1| = 1.
The distance from 4 to 0 is |4| = 4.
The distance from 8 to 0 is |8| = 8.
Thus, the closest number to 0 in the array is 1.
```

Example 2:

```text
Input:
nums = [2,-1,1]
Output:
1
Explanation:
1 and -1 are both the closest numbers to 0, so 1 being larger is returned.
```

Constraints:

- 1 <= n <= 1000
- -10 ^5 <= nums[i] <= 10 ^5

## Enfoque

Recorre el arreglo una vez y conserva el numero con menor valor absoluto. En empate por valor absoluto, se elige el mayor numero para privilegiar el positivo.

## Diagrama del algoritmo

```mermaid
flowchart TD
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
    I --> C
```

## Desglose paso a paso del codigo

1. Inicializa `best` con el primer valor para tener una referencia valida desde el inicio.
2. Recorre los valores restantes y compara `abs(value)` contra `abs(best)`.
3. Si `value` esta mas cerca de cero, actualiza `best`.
4. Si hay empate de distancia (`abs(value) == abs(best)`), elige el mayor valor para priorizar el positivo.
5. Al final retorna `best` como el numero mas cercano a cero segun la regla del problema.

## Por que funciona

El algoritmo mantiene un invariante: despues de procesar cada posicion, `best` es la mejor respuesta entre los elementos vistos. Como cada nuevo elemento compite contra ese mejor parcial, al terminar el recorrido se obtiene la solucion global correcta.

## Complejidad

Tiempo O(n), espacio O(1).

## Evidencia

Pendiente de adjuntar screenshot de envio exitoso.
