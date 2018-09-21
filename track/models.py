"""Contains the Visit model."""

import os
from datetime import datetime, timedelta
import pytz
from django.db import models

class Visit(models.Model):
    """A visit to the Django app."""

    class Meta:
        ordering = ["-datetime"]

    datetime = models.DateTimeField()
    path = models.CharField(max_length=256, blank=True, null=True)
    ip_hash = models.CharField(max_length=64, blank=True, null=True)
    referer = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    agent = models.CharField(max_length=1024, blank=True, null=True)

    @staticmethod
    def from_day(dt):
        """Gets all the visits from a given day. The function takes an _aware_
        datetime, and gets the visits which took place on that day, during that
        timezone.

        :param datetime dt: the aware datetime to filter by."""

        start = datetime(
         dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=dt.tzinfo
        ).astimezone(pytz.UTC).replace(tzinfo=None)
        end = start + timedelta(days=1)
        return Visit.objects.filter(datetime__gt=start, datetime__lt=end)
