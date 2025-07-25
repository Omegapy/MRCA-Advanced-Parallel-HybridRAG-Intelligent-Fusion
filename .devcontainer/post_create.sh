#!/usr/bin/env bash

echo "Setting up MRCA development environment with Docker support..."

# Update pip first
echo "Updating pip..."
pip3 install --upgrade pip

# Install main requirements
echo "Installing MRCA dependencies..."
pip3 install -r requirements.txt

# Ensure we have all necessary directories
echo "Creating necessary directories..."
mkdir -p data
mkdir -p .streamlit

# Set proper permissions
echo "Setting permissions..."
chmod +x launch_app.py
chmod +x launch.sh

# Initialize Docker service (Docker-in-Docker)
echo "Initializing Docker service..."
if ! pgrep -x dockerd > /dev/null; then
    echo "Starting Docker daemon..."
    sudo dockerd > /dev/null 2>&1 &
    sleep 5
fi

# Verify Docker is working
echo "Verifying Docker installation..."
if command -v docker >/dev/null 2>&1; then
    echo "✅ Docker CLI available"
    docker --version
else
    echo "❌ Docker CLI not found"
fi

if command -v docker-compose >/dev/null 2>&1; then
    echo "✅ Docker Compose available"
    docker-compose --version
elif command -v docker > /dev/null 2>&1 && docker compose version > /dev/null 2>&1; then
    echo "✅ Docker Compose (v2) available"
    docker compose version
else
    echo "❌ Docker Compose not found"
fi

echo "MRCA development environment setup complete!"
echo ""
echo "🚀 Available launch methods:"
echo "  1. Docker (Recommended): docker-compose up --build -d"
echo "  2. Python Direct: python3 launch_app.py"
echo ""
echo "🌐 Access points after launch:"
echo "  - Frontend: http://localhost:8501"
echo "  - Backend: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"