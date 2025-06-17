FROM python:3.12-alpine

# Update the package lists for upgrades for packages that need upgrading, as well as new packages that have just come to the repositories.
RUN apk update

# Install the packages
RUN apk add --no-cache \
    gdal \
    gdal-dev \
    gcc \
    musl-dev \
    libpq-dev \
    geos-dev

# Upgrade pip
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
COPY clioguesser_backend/ ./clioguesser_backend/

# Install Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/clioguesser_backend
