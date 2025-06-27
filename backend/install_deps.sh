#!/bin/bash
# Script to install dependencies in Azure App Service

echo "Installing Python dependencies..."

# Try different Python paths
if [ -f "/opt/python/3.11/bin/python3" ]; then
    /opt/python/3.11/bin/python3 -m pip install -r requirements.txt
elif [ -f "/usr/local/bin/python3" ]; then
    /usr/local/bin/python3 -m pip install -r requirements.txt
else
    # Use the virtual environment if it exists
    if [ -d "antenv" ]; then
        source antenv/bin/activate
        pip install -r requirements.txt
    else
        # Create virtual environment
        python3 -m venv antenv
        source antenv/bin/activate
        pip install -r requirements.txt
    fi
fi

echo "Dependencies installed!"