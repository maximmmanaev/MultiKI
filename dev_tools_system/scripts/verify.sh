#!/usr/bin/env bash
set -euo pipefail

echo "[verify] MultiKI dev tools system verification started"

if [ ! -f "dev_tools_system/AGENTS.md" ]; then
  echo "[verify] ERROR: dev_tools_system/AGENTS.md not found"
  exit 1
fi

if [ ! -f "dev_tools_system/docs/DEV_SYSTEM.md" ]; then
  echo "[verify] ERROR: dev_tools_system/docs/DEV_SYSTEM.md not found"
  exit 1
fi

if [ ! -d ".github/ISSUE_TEMPLATE" ]; then
  echo "[verify] ERROR: .github/ISSUE_TEMPLATE not found"
  exit 1
fi

echo "[verify] Base structure is valid"
echo "[verify] OK"
