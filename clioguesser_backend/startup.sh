#!/bin/sh

# Set the process ID of the main application
APP_PID=0

cleanup() {
  echo "SIGTERM received by shell (PID $$), initiating graceful shutdown..."

  # If your application is a long-running process that was put in background
  if [ "$APP_PID" -ne 0 ]; then
    echo "Sending SIGTERM to application (PID $APP_PID)..."
    kill -TERM "$APP_PID"
    # Wait for the application to actually terminate
    wait "$APP_PID" || true # '|| true' to prevent script from exiting if wait fails
  fi

  python push.py

  echo "Application has terminated. Exiting container."
  exit 0
}

# Trap signals for the shell process itself
trap 'cleanup' TERM
trap 'cleanup' INT # SIGINT will also call cleanup now

echo "Pulling"
python pull.py || exit 1

echo "Starting ClioGuesser backend (shell is PID $$)..."

# Run the application in the background
# The shell remains PID 1 and can catch signals
gunicorn clioguesser_backend.wsgi:application --bind 0.0.0.0:80 --workers 3 --timeout 120 --log-level info &
APP_PID=$! # Store the PID of the background process

echo "Application (PID $APP_PID) started. Waiting for signals..."

# Wait indefinitely for the background process to finish or for a signal
# 'wait' command makes the shell pause until all its background jobs are done.
# If a signal is caught, the trap handler executes, then the script exits.
wait "$APP_PID"

echo "Script finished naturally (sleep ended)."
