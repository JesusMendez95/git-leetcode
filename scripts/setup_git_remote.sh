#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_NAME="${1:-git-leetcode}"
REMOTE_URL="https://github.com/JesusMendez95/${REPO_NAME}.git"

cd "${ROOT_DIR}"

if [ ! -d .git ]; then
  git init
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "${REMOTE_URL}"
else
  git remote add origin "${REMOTE_URL}"
fi

echo "Remote origin configurado: ${REMOTE_URL}"
echo "Asegurate de que el repo exista en GitHub y tengas credenciales (SSH o token)."
