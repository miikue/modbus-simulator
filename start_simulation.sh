#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Function to clean up background processes
cleanup() {
    echo "Shutting down simulation..."
    # Kill all background jobs of this script
    kill $(jobs -p) 2>/dev/null
    echo "All simulation processes stopped."
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo "Starting Modbus server..."
python simulator.py &
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"

wait
