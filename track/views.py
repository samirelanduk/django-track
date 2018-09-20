from datetime import datetime, date
import pytz
from collections import Counter
from django.shortcuts import render
from django.conf import settings
from .models import Visit

def analytics(request):
    try:
        timezone = pytz.timezone(settings.TRACK_TZ)
    except:
        timezone = pytz.UTC

    now = datetime.now(timezone)
    visits = list(Visit.from_day(now))
    for v in visits:
        v.time = (v.datetime + now.tzinfo.utcoffset(now)).time()

    histograms = [
     (sorted(dict(Counter([getattr(v, f) for v in visits])).items(),
      key=lambda r: r[1], reverse=True), f) for f in ["path", "country", "city"]
    ]

    return render(request, "track/analytics.html", {
     "date": now.date(),
     "visits": visits,
     "histograms": histograms
    })
