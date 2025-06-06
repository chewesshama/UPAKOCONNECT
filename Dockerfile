# Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libssl-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure wait-for-it.sh is executable in Docker
RUN chmod +x wait-for-it.sh
