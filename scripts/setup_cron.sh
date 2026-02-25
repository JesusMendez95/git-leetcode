#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -x "${ROOT_DIR}/.venv/bin/python" ]; then
  DEFAULT_PYTHON="${ROOT_DIR}/.venv/bin/python"
else
  DEFAULT_PYTHON="python3"
fi
PYTHON_BIN="${PYTHON_BIN:-$DEFAULT_PYTHON}"
RUN_AT="${1:-08:00}"

HOUR="${RUN_AT%:*}"
MINUTE="${RUN_AT#*:}"

CRON_LINE="${HOUR} ${MINUTE} * * * cd \"${ROOT_DIR}\" && ${PYTHON_BIN} scripts/run_daily.py >> logs/daily.log 2>&1"

mkdir -p "${ROOT_DIR}/logs"

TMP_FILE="$(mktemp)"
crontab -l > "${TMP_FILE}" 2>/dev/null || true

if ! grep -Fq "scripts/run_daily.py" "${TMP_FILE}"; then
  printf "%s\n" "${CRON_LINE}" >> "${TMP_FILE}"
  crontab "${TMP_FILE}"
  echo "Cron agregado: ${CRON_LINE}"
else
  echo "Ya existe una entrada de cron para run_daily.py"
fi

rm -f "${TMP_FILE}"
