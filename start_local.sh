#!/bin/bash

echo "IDEPocket Quick Start..."

if [ ! -f "Backend/.env" ]; then
    echo ".env file not found. Copying .env.example..."
    cp Backend/.env.example Backend/.env
    echo "Please configure your API keys in Backend/.env and restart the script."
    exit 1
fi

echo "Installing dependencies..."
pip install -e ./shared
pip install -r Backend/requirements.txt
pip install -r Terminal_Agent/requirements.txt

echo "Starting Backend in background..."
python Backend/main.py &
BACKEND_PID=$!

echo "Starting Terminal Agent..."
python Terminal_Agent/main.py

trap "kill $BACKEND_PID" EXIT
