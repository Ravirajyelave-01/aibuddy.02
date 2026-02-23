#!/bin/bash

# Production run script with proper WebSocket support

PORT=${PORT:-5000}
WORKERS=${WORKERS:-1}
TIMEOUT=${TIMEOUT:-120}

echo "Starting Voice Assistant Server..."
echo "Port: $PORT"
echo "Workers: $WORKERS"
echo "Timeout: $TIMEOUT"

gunicorn \
  --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
  -w "$WORKERS" \
  -b 0.0.0.0:"$PORT" \
  --timeout "$TIMEOUT" \
  --access-logfile - \
  --error-logfile - \
  wsgi:app
