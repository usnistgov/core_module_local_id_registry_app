SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    # Django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Local apps
    "tests",
]
SERVER_URI = "http://hostname.com"

PID_XPATH = "mock.xpath"

PID_FORMAT = r"[a-zA-Z0-9_\-]+"

ID_PROVIDER_SYSTEM_NAME = "mock_provider"

ID_PROVIDER_PREFIXES = ["mock_prefix"]
