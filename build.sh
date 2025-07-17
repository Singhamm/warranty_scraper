#!/bin/bash

# Exit on error
set -e

# Install system dependencies needed by Playwright
apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 \
    libgbm-dev libasound2 libxshmfence1 libxcomposite1 \
    libxrandr2 libxdamage1 libpango-1.0-0 libx11-xcb1 \
    libgdk-pixbuf2.0-0 libxinerama1 fonts-liberation \
    wget curl unzip xvfb

# Upgrade pip and install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium

# Optional: Run tests (ignore failure to avoid breaking deploy)
python -m pytest tests/ -v || true
