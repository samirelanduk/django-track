
import os
from datetime import datetime, timedelta
import pytz
from django.db import models
from django.contrib.gis.geoip2 import GeoIP2

class Visit(models.Model):

    class Meta:
        ordering = ["-datetime"]

    datetime = models.DateTimeField()
    path = models.CharField(max_length=256, blank=True, null=True)
    IP = models.CharField(max_length=64, blank=True, null=True)
    referer = models.CharField(max_length=256, blank=True, null=True)

    country_lookups = {}
    city_lookups = {}

    @staticmethod
    def from_day(dt):
        start = datetime(
         dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=dt.tzinfo
        ).astimezone(pytz.UTC).replace(tzinfo=None)
        end = start + timedelta(days=1)
        return Visit.objects.filter(datetime__gt=start, datetime__lt=end)


    @property
    def country(self):
        try:
            return self.country_lookups[self.IP]
        except:
            try:
                country = GeoIP2().country(self.IP)["country_name"]
            except: country = "Unknown"
            self.country_lookups[self.IP] = country
            return country


    @property
    def city(self):
        try:
            return self.city_lookups[self.IP]
        except:
            try:
                city = GeoIP2().city(self.IP)["city"]
            except: city = "Unknown"
            self.city_lookups[self.IP] = city
            return city
