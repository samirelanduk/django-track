from datetime import datetime, date, timedelta
import pytz
from collections import Counter
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .models import Visit

@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def analytics(request):
    try:
        timezone = pytz.timezone(settings.TRACK_TZ)
    except:
        timezone = pytz.UTC

    now = datetime.now(timezone)
    try:
        year, month, day = [int(x) for x in request.GET["day"].split("-")]
        now = timezone.localize(datetime(year, month, day, now.hour, now.minute, now.second))
    except: pass
    visits = list(Visit.from_day(now))
    for v in visits:
        v.time = (v.datetime + now.tzinfo.utcoffset(now)).time()

    data = [{
     "hour": v.time.hour, "minute": v.time.minute,
     "second": v.time.second,
     "seconds": (v.time.hour * 3600) + (v.time.minute * 60) + v.time.second,
     "path": v.path, "country": v.country or "Unknown", "city": v.city or "Unknown",
     "referer": v.referer or "", "IP": v.ip_hash,
     "source": v.referer.split("/")[2] if v.referer and v.referer.count("/") > 2 else "Unknown",
     "agent": v.agent or "Unknown"
    } for v in visits]

    return render(request, "track/analytics.html", {
     "date": now.date(),
     "yesterday": now.date() - timedelta(days=1),
     "tomorrow": now.date() + timedelta(days=1),
     "data": data,
    })
