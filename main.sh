#!/bin/bash
set -e
date=$(date +'%FT%T')
if [ ! -d "venv" ]; then
  echo $date "Virtual environment not found. Creating one."
  python3 -m venv venv
  echo $date  "Activating virtual environment"
  source venv/bin/activate
  echo $date  "Installing dependencies"
  pip install -r requirements.txt
else
  echo $date "Virtual environment already exists."
  echo $date "Activating virtual environment"
  source venv/bin/activate
fi
echo $date "Running main.py"
while true; do
  python3 ./main.py
  echo $date "Script exited. Waiting for 15 seconds before the next run."
  sleep 15
done
