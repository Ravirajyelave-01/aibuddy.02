#!/bin/bash

# Voice Assistant Setup Script
# Installs all dependencies and builds the React app

set -e

echo "==================================="
echo "Voice Assistant Setup"
echo "==================================="

# Step 1: Install Python dependencies
echo ""
echo "Step 1: Installing Python dependencies..."
pip install -r requirements-deploy.txt

# Step 2: Build React app
echo ""
echo "Step 2: Building React application..."
cd react-app || exit 1

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

echo "Building React app..."
npm run build

cd ..

echo ""
echo "==================================="
echo "✓ Setup Complete!"
echo "==================================="
echo ""
echo "To start the application:"
echo ""
echo "Development mode:"
echo "  python app.py"
echo ""
echo "Production mode:"
echo "  gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 wsgi:app"
echo ""
echo "Visit http://localhost:5000"
echo ""
