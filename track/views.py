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

    data = [{
     "hour": v.time.hour, "minute": v.time.minute,
     "second": v.time.second,
     "seconds": (v.time.hour * 3600) + (v.time.minute * 60) + v.time.second,
     "path": v.path, "country": v.country, "city": v.city,
     "referer": v.referer or ""
    } for v in visits]

    return render(request, "track/analytics.html", {
     "date": now.date(),
     "data": data,
    })
