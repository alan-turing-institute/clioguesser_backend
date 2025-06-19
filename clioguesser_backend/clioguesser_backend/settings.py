from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
# You may want to create with $(openssl rand -hex 32)
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [x.strip() for x in env("DJANGO_ALLOWED_HOSTS", default="*").split(",")]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",  # Add this for GIS support
    "core",  # Your core app
    "corsheaders",
]

CORS_ALLOWED_ORIGINS = [
    x.strip()
    for x in env("CORS_ALLOWED_ORIGINS", default="http://localhost:5173").split(",")
]

CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clioguesser_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",  # This is the name of the database table for your cache
        "TIMEOUT": 3600,
        "OPTIONS": {
            "MAX_ENTRIES": 500,  # Maximum number of entries allowed in the cache (default is 300)
            # "CULL_FREQUENCY": 3, # How often to cull expired entries (default is 3)
        },
    }
}

RATELIMIT_USE_CACHE = "default"

WSGI_APPLICATION = "clioguesser_backend.wsgi.application"
ASGI_APPLICATION = "clioguesser_backend.asgi.application"

db_path: Path = env("DB_NAME", cast=Path)
if db_path.parts[1] == "home":
    # Special case for Azure App Service, where we need to copy
    # the db from blob storage to the semi-persistent /home directory.
    assert db_path.exists(), "Expected database file to exist already"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        # Path to your SQLite database file.
        # Will be created if it doesn't exist.
        "NAME": db_path,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Geospatial stuff: modify the paths to the libraries for your system setup
GEOGRAPHIC_DB = True
