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

    def middleware(request):
        track = not any(re.search(p, request.path) for p in path_exclude)
        if track: track = request.META["HTTP_HOST"] not in host_exclude
        
        if track:
            try:
                if request.path.startswith("/" + settings.MEDIA_URL): track = False
            except: pass

            if track:
                Visit.objects.create(
                 datetime=datetime.utcnow(),
                 path=request.path,
                 IP=request.META.get("REMOTE_ADDR"),
                 referer=request.META.get("HTTP_REFERER")
                )

        response = get_response(request)
        return response

    return middleware
