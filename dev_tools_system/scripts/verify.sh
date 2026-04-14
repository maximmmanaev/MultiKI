#!/usr/bin/env bash
set -euo pipefail

echo "[verify] MultiKI dev tools system verification started"

if [ ! -r "dev_tools_system/scripts/verify.sh" ]; then
  echo "[verify] ERROR: run this script from the repository root"
  exit 1
fi

if [ ! -r "dev_tools_system/AGENTS.md" ]; then
  echo "[verify] ERROR: dev_tools_system/AGENTS.md is not readable"
  exit 1
fi

if [ ! -r "dev_tools_system/docs/DEV_SYSTEM.md" ]; then
  echo "[verify] ERROR: dev_tools_system/docs/DEV_SYSTEM.md is not readable"
  exit 1
fi

if [ ! -d ".github/ISSUE_TEMPLATE" ] || [ ! -r ".github/ISSUE_TEMPLATE" ]; then
  echo "[verify] ERROR: .github/ISSUE_TEMPLATE does not exist or is not readable"
  exit 1
fi

echo "[verify] Base structure is valid"
echo "[verify] OK"
