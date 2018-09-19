from datetime import datetime
from django.conf import settings
from .models import Visit

def inspect_response(get_response):

    def middleware(request):
        track = True
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
