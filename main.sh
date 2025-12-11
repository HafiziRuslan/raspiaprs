#!/bin/bash
set -e
date=$(date +'%F %T')

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

if command_exists uv; then
  echo "$date - ✅ uv is installed."
else
  echo -n "$date - ❌ uv is NOT installed."
  echo " -> Installing uv"
  wget -qO- https://astral.sh/uv/install.sh | sh
fi

if [ ! -d ".venv" ]; then
  echo "$date - Virtual environment not found, creating one."
  uv venv
  echo "$date - Activating virtual environment"
  source .venv/bin/activate
  echo "$date - Installing dependencies"
  uv sync
else
  echo -n "$date - Virtual environment already exists."
  echo " -> Activating virtual environment"
  source .venv/bin/activate
  echo "$date - Updating dependencies"
  uv sync
fi

echo "$date - Running main.py"
while true; do
  uv run -s ./main.py
  echo "$date - Script exited. Waiting for 15 seconds before the next run."
  sleep 15
done
