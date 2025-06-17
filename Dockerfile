FROM python:3.12-alpine

# Declare build-time arguments
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

# Export them to ENV for manage.py to see them
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

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

COPY requirements-alpine.txt .
COPY clioguesser_backend/ ./clioguesser_backend/

# Install Python dependencies
RUN pip install -r requirements-alpine.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/clioguesser_backend
