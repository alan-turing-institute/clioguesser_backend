import os

from django.core.wsgi import get_wsgi_application

from clioguesser_backend.sync import register_shutdown_hook

register_shutdown_hook()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clioguesser_backend.settings")
application = get_wsgi_application()
