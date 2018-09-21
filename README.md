# Django-Track

|travis| |coveralls| |pypi|

.. |travis| image:: https://api.travis-ci.org/samirelanduk/django-track.svg
  :target: https://travis-ci.org/samirelanduk/django-track/

.. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/django-track/badge.svg
  :target: https://coveralls.io/github/samirelanduk/django-track/

.. |pypi| image:: https://img.shields.io/pypi/pyversions/django-track.svg
  :target: https://pypi.org/project/django-track/

Track is a lightweight analytics plugin that provides clean, easy-to-read analytics with zero cookies.

## How to Install

1. ``$ pip install django-track``
2. Add ``track`` to your list of installed apps.
3. Add ``track.middleware.inspect_response`` to your list of middleware.
4. Run ``python manage.py migrate`` to create the single ``Visit`` model.

Once you've done those four things, the bare functionality of track is enabled - every request to your application will be saved as a ``Visit`` record. If you plan on processing this data yourself no further action is needed. If you want the single-page analytics viewer, there are a few more steps:

5. In your ``urls.py``, you need to point some URL at ``track.views.analytics``. For example: ``path("analytics/", track.views.analytics)``.
6. Ensure that the built-in ``django.contrib.staticfiles`` is installed.

That's it. Now you can to whatever URL you chose and see your page views.

You will notice that every city and country is listed as 'Unknown' as it is however. track only stores hashed IP addresses - location information is calculated from this when the request comes in, and to do this, a geolocation binary needs to be installed:

7. Download two geolocation binaries from [this page](https://dev.maxmind.com/geoip/geoip2/geolite2/), - the city and countries binaries specifically.
8. Put them somewhere in your system.
9. In your django settings.py, set ``GEOIP_PATH`` to wherever those files are now.

And now when you view the analytics page, the location information will be shown.

(The reason track doesn't have this built in is because the database files are a bit unwieldy to package into a Python library, and not every site might want to use this third party service.)

Finally, you can customise track with various settings:

10. ``TRACK_TZ`` will determine the pytz timezone times are shown in. All times are stored in the database as UTC regardless of what this is set to. For example: ``TRACK_TZ = "Europe/London"``.
11. ``TRACK_PATH_EXCLUDE`` can be a list of regex strings, and any request whose path matches will not be tracked. For example ``TRACK_PATH_EXCLUDE = [r"\.ico$", r"^/admin"]``.
12. ``TRACK_HOST_EXCLUDE`` can be a list of strings, and any request for a hostname in this list will not be tracked. For example: ``TRACK_HOST_EXCLUDE = ["test.example.com", "localhost"]``.

## Authentication

The analytics page can only be viewed by users who are logged in as superusers.
