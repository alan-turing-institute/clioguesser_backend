FROM python:3.11-bullseye

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
RUN apt-get update -y

# Install the packages
RUN apt-get install -y gdal-bin libgdal-dev libgeos++-dev libgeos-c1v5 libgeos-dev libgeos-doc unzip
# Install pip
#RUN apt-get install -y python3-pip

RUN ln -s /usr/lib/libgdal.so.28 /usr/lib/libgdal.so.30

# Upgrade pip
#RUN python3 -m pip install --upgrade pip
RUN pip install "django-geojson[field]"

WORKDIR /app

COPY . .

# Copy requirements.txt file into the Docker image
# Install Python dependencies
RUN pip install -r requirements.txt

# Install django-geojson
RUN unzip -o cliopatria/cliopatria.geojson.zip -d clioguesser_backend/data

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/clioguesser_backend
