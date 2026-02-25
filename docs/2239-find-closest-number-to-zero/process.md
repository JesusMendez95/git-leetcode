# Proceso de resolucion - Find Closest Number to Zero

## Enfoque

Recorre el arreglo una vez y conserva el numero con menor valor absoluto. En empate por valor absoluto, se elige el mayor numero para privilegiar el positivo.

## Complejidad

Tiempo O(n), espacio O(1).

## Validacion recomendada

1. Ejecutar casos simples (positivos, negativos, empate de valor absoluto).
2. Verificar que, en empate, se elige el numero positivo.
3. Confirmar envio exitoso en LeetCode y adjuntar screenshot en `docs/2239-find-closest-number-to-zero/screenshots/`.
