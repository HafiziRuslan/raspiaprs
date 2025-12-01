#!/bin/bash
set -e
if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Creating one."
  python3 -m venv venv
  echo "Activating virtual environment"
  source venv/bin/activate
  echo "Installing dependencies"
  pip install -r requirements.txt
else
  echo "Virtual environment already exists."
  echo "Activating virtual environment"
  source venv/bin/activate
fi
echo "Running main.py"
while true; do
  python3 ./main.py
done
