# Git LeetCode Daily Automation

Automatiza un flujo diario para retos de LeetCode usando el roadmap de AlgoMap:

- extrae retos estructurados desde `https://algomap.io/roadmap`,
- genera solucion en Python,
- crea documentacion con descripcion del problema,
- genera explicacion tecnica con diagrama Mermaid,
- y publica cambios a GitHub (cron local).

## Estructura

- `data/algomap_challenges.json`: catalogo de retos.
- `solutions/python/`: soluciones.
- `docs/<id-slug>/process.md`: documentacion completa del reto.
- `state/daily_state.json`: historial de ejecuciones.

## Instalacion

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuracion

```bash
cp .env.example .env
```

Valores recomendados en `.env`:

```env
GIT_REMOTE_URL=git@github.com:JesusMendez95/git-leetcode.git
DEFAULT_LANGUAGE=python
GITHUB_USERNAME=JesusMendez95
ROADMAP_URL=https://algomap.io/roadmap
```

Si necesitas crear/configurar `origin`:

```bash
bash scripts/setup_git_remote.sh git-leetcode
```

## Ejecucion diaria

Ejecucion local:

```bash
python scripts/run_daily.py
```

## Cron local

```bash
bash scripts/setup_cron.sh 08:00
```

El log queda en `logs/daily.log`.

## Notas de documentacion

- `process.md` incluye metadata, descripcion oficial del problema, solucion, enfoque, diagrama Mermaid, desglose del codigo, justificacion del algoritmo y complejidad.
