#!/bin/bash

# Kill any process running on port 8000
echo "Checking for processes on port 8000..."
PORT=8000
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port $PORT..."
    kill -9 $PID
    echo "Process killed successfully."
else
    echo "No process found on port $PORT."
fi

# Wait a moment for the port to be released
sleep 1

# Start the application
echo "Starting the application..."
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
