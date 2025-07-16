# Base image with Python
FROM python:3.10-slim

# Install system dependencies for Playwright and headless browser support
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libxss1 \
    libxtst6 \
    libgtk-3-0 \
    libgtk-4-1 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libxshmfence1 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libxkbcommon0 \
    libxinerama1 \
    libgl1-mesa-glx \
    libgl1 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libopengl0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright and browsers
RUN playwright install --with-deps

# Copy project files into container
COPY . /app
WORKDIR /app

# Set Streamlit default port
ENV STREAMLIT_SERVER_PORT=8501

# Start command (can be overridden by devcontainer.json)
CMD ["streamlit", "run", "streamlit_app.py"]
