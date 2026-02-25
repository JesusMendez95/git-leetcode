# Git LeetCode Daily Automation

Proyecto en Python para:

- Extraer retos estructurados desde `https://algomap.io/roadmap`.
- Resolver retos (inicialmente con registry de solvers por LeetCode ID).
- Generar documentacion por reto (`README.md` y `process.md`).
- Adjuntar screenshot de envio exitoso.
- Publicar automaticamente a GitHub una vez al dia (cron local).

## Estructura

- `data/algomap_challenges.json`: catalogo de retos extraidos.
- `solutions/python/`: soluciones en Python.
- `docs/<id-slug>/README.md`: documentacion de la solucion.
- `docs/<id-slug>/process.md`: proceso de resolucion.
- `docs/<id-slug>/screenshots/`: evidencia de envio exitoso.
- `state/daily_state.json`: historial de ejecuciones diarias.
- `scripts/run_daily.py`: orquestador diario.

## Instalacion

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuracion inicial

1. Crear `.env` desde `.env.example` y completar `GIT_REMOTE_URL`.
   - O usa el helper: `bash scripts/setup_git_remote.sh git-leetcode`
2. Exportar variables (si no usas dotenv):

```bash
export ROADMAP_URL="https://algomap.io/roadmap"
export GIT_REMOTE_URL="https://github.com/JesusMendez95/<tu-repo>.git"
```

3. Generar catalogo:

```bash
python scripts/bootstrap_catalog.py
```

## Flujo diario

```bash
python scripts/run_daily.py --allow-missing-screenshot --skip-push
```

Despues de enviar el reto en LeetCode, guarda screenshot en:

`docs/<id-slug>/screenshots/<YYYY-MM-DD>-success.png`

Luego ejecuta:

```bash
python scripts/run_daily.py
```

Eso genera commit y push si el remote esta configurado y hay screenshot.

## Automatizacion con cron local

```bash
bash scripts/setup_cron.sh 08:00
```

Esto ejecuta `scripts/run_daily.py` todos los dias a las 08:00 y deja logs en `logs/daily.log`.

## Nota sobre solvers

El proyecto viene con un solver implementado:

- `2239 - Find Closest Number to Zero`

Para agregar mas retos, extiende `src/git_leetcode/solver.py` con nuevos IDs.
