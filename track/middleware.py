from datetime import datetime
import re
from django.conf import settings
from django.urls import reverse
from .models import Visit
from .views import analytics

def inspect_response(get_response):

    exclude = settings.__dict__.get("TRACK_EXCLUDE", [])
    exclude += [reverse(analytics)]

    def middleware(request):
        track = not any(re.search(p, request.path) for p in exclude)
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
