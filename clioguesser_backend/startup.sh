#!/bin/sh

# trap sigterm
trap 'echo "SIGTERM received, shutting down..."; exit 0' TERM
trap 'echo "SIGINT received, shutting down..."; exit 0' INT

echo "Starting ClioGuesser backend..."
sleep 10000