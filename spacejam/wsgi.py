"""
WSGI config for spacejam project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

project_home = u'/home/ubuntu/spacejam'
if project_home not in sys.path:
    sys.path.append(project_home)

os.environ["DJANGO_SETTINGS_MODULE"] = "spacejam.settings"

application = get_wsgi_application()
