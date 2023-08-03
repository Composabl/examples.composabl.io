#!/bin/bash
HOST=${HOST:-"[::]"}
PORT=${PORT:-"50051"}

echo "Available ROMs:"
poetry run python -c "import ale_py.roms as roms; print(roms.__all__)"

echo "Starting..."
poetry run main