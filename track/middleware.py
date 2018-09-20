from datetime import datetime
import re
from django.conf import settings
from django.urls import reverse
from .models import Visit
from .views import analytics

def inspect_response(get_response):

    try:
        path_exclude = settings.TRACK_PATH_EXCLUDE + [reverse(analytics)]
    except:
        path_exclude = [reverse(analytics)]

    try:
        host_exclude = settings.TRACK_HOST_EXCLUDE
    except:
        host_exclude = []

    IP_TRY = [
     "HTTP_X_FORWARDED_FOR",
     "X_FORWARDED_FOR",
     "HTTP_CLIENT_IP",
     "HTTP_X_REAL_IP",
     "HTTP_X_FORWARDED",
     "HTTP_X_CLUSTER_CLIENT_IP",
     "HTTP_FORWARDED_FOR",
     "HTTP_FORWARDED",
     "HTTP_VIA",
     "REMOTE_ADDR"
    ]

    def middleware(request):
        track = not any(re.search(p, request.path) for p in path_exclude)
        if track: track = request.META["HTTP_HOST"] not in host_exclude

        if track:
            try:
                if request.path.startswith("/" + settings.MEDIA_URL): track = False
            except: pass

            ip = None
            for attempt in IP_TRY:
                possible = request.META.get(attempt)
                raise Exception(possible)
                if possible:
                    ip = possible
                    break

            if track:
                Visit.objects.create(
                 datetime=datetime.utcnow(),
                 path=request.path,
                 IP=ip,
                 referer=request.META.get("HTTP_REFERER")
                )

        response = get_response(request)
        return response

    return middleware
