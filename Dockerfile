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
    geos-dev \
    libspatialite-dev \
    tini \
    openssh

# Create SSH runtime directory
RUN mkdir -p /var/run/sshd

# Upgrade pip
RUN pip install --upgrade pip

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY clioguesser_backend/ ./clioguesser_backend/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/clioguesser_backend

ENTRYPOINT ["tini", "--"]
CMD ["./startup.sh"]
