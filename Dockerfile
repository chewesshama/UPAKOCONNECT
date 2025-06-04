FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install all needed system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libssl-dev \
    curl \
    && apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
