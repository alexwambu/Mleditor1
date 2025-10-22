#!/bin/bash
echo "Starting Ethereum Builder..."
python3 main.py &
uvicorn main:app --host 0.0.0.0 --port 8000
