#!/usr/bin/env bash
set -euo pipefail

# Single dev command to run both Flask backend and Next frontend for local dev.
# Usage: ./dev.sh
# It will:
#  - export BACKEND_HOST and BACKEND_PORT for the frontend
#  - start the Flask app on BACKEND_PORT if nothing is listening there
#  - cd into my-stock-portfolio and run `npm run dev` (installing deps if needed)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export BACKEND_PORT=${BACKEND_PORT:-5000}
export BACKEND_HOST=${BACKEND_HOST:-http://localhost:${BACKEND_PORT}}

echo "Using BACKEND_HOST=${BACKEND_HOST} BACKEND_PORT=${BACKEND_PORT}"

start_backend() {
  # If something is listening on the backend port, skip starting Flask
  if lsof -iTCP:${BACKEND_PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Port ${BACKEND_PORT} already in use; assuming backend already running."
    BACKEND_PID=""
    return
  fi

  echo "Starting Flask backend..."
  (cd "${ROOT_DIR}" && python3 app.py) &
  BACKEND_PID=$!
  echo "Flask started with PID ${BACKEND_PID}"

  # wait a short time for server to come up
  sleep 1

  # Wait for health endpoint
  echo "Waiting for backend health..."
  attempts=0
  max_attempts=15
  until curl -sSf "${BACKEND_HOST}/health" >/dev/null 2>&1; do
    attempts=$((attempts+1))
    if [ $attempts -ge $max_attempts ]; then
      echo "Backend did not become healthy after $max_attempts attempts."
      return
    fi
    echo "  waiting for backend... ($attempts/$max_attempts)"
    sleep 1
  done
  echo "Backend healthy."
}

cleanup() {
  echo "Cleaning up..."
  if [ -n "${BACKEND_PID:-}" ]; then
    echo "Killing backend PID ${BACKEND_PID}"
    kill "${BACKEND_PID}" 2>/dev/null || true
  fi
  exit 0
}

trap cleanup SIGINT SIGTERM EXIT

start_backend

echo "Starting Next.js dev server..."
cd "${ROOT_DIR}/my-stock-portfolio"

# Install node deps if node_modules missing
if [ ! -d node_modules ]; then
  echo "Installing frontend npm dependencies (this may take a moment)..."
  npm install
fi

# Run Next dev in foreground. When it exits, cleanup() will run to stop the backend.
npm run dev
