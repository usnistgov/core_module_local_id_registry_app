""" Test settings
"""

SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    # Django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Local apps
    "core_main_app",
    "core_main_registry_app",
    "core_parser_app",
    "core_curate_app",
    "tests",
]

# In-memory test DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

SERVER_URI = "http://hostname.com"

PID_XPATH = "mock.xpath"

PID_FORMAT = r"[a-zA-Z0-9_\-]+"

ID_PROVIDER_SYSTEM_NAME = "mock_provider"

ID_PROVIDER_PREFIXES = ["mock_prefix"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
