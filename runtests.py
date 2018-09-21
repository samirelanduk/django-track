
#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

def runtests():
    if not settings.configured:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:"
            }
        }
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                "track",
            ),
            ROOT_URLCONF="",
            MIDDLEWARE_CLASSES=(
                "track.middleware.inspect_request"
            )
        )

    if django.VERSION >= (1, 7):
        django.setup()
    failures = call_command(
        "test", "tests", interactive=False, failfast=False)
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
