import os
import sys
from datetime import datetime
import pytz
import testarsenal
from django.test import TestCase
from track.views import analytics

class AnalyticsTests(testarsenal.DjangoTest):

    def test_view_uses_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(analytics, request, "track/analytics.html")
