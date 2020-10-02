""" Core module loval id registry settings

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

LOCAL_ID_LENGTH = getattr(settings, "LOCAL_ID_LENGTH", 20)
""" int: length used to generate the unique local id.
"""

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])
""" :py:class:`list`: List of apps installed.
"""

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")
""" str: URI of the server
"""
