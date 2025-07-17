#!/bin/bash
set -e  # Stop script on first error

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎭 Installing Playwright Chromium browser (headless)..."
playwright install chromium

echo "✅ Build script completed successfully."

# Optional: Run tests only if needed (uncomment below)
# echo "🧪 Running Pytest suite..."
# python -m pytest tests/ -v
