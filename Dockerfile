FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    alsa-utils \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn flask-socketio python-socketio

# Copy Python backend
COPY *.py ./

# Copy React build (build React app first)
COPY react-app/build ./templates
COPY react-app/build/static ./public/build/static

# Expose port
EXPOSE 5000

# Run the Flask app with gunicorn
CMD ["gunicorn", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "--timeout", "120", "wsgi:app"]
