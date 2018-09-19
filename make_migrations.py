#!/usr/bin/env python

import os
import sys
import django
from django.core.management import execute_from_command_line

SECRET_KEY = "."
INSTALLED_APPS = ["track"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __name__)
django.setup()

execute_from_command_line(["", "makemigrations", "track"])
