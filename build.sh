#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run tests (optional)
python -m pytest tests/ -v