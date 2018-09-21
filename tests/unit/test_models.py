import os
import sys
from datetime import datetime
import pytz
from django.test import TestCase
from track.models import Visit

class VisitTests(TestCase):

    def test_can_get_visits_from_day(self):
        visits = []
        for d in [
         datetime(1990, 9, 1, 12, 0, 0), datetime(1990, 9, 1, 18, 0, 0),
         datetime(1990, 9, 1, 22, 0, 0), datetime(1990, 9, 2, 3, 0, 0)
        ]:
            visits.append(Visit.objects.create(datetime=d))
        utc = pytz.UTC.localize(datetime(1990, 9, 1, 12, 0, 0))
        moscow = pytz.timezone("Europe/Moscow").localize(datetime(1990, 9, 1, 12, 0, 0))
        self.assertEqual(list(Visit.from_day(utc)), visits[:3][::-1])
        self.assertEqual(list(Visit.from_day(moscow)), visits[:2][::-1])
