from datetime import datetime
import re
from django.core.signing import Signer
from django.contrib.gis.geoip2 import GeoIP2
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
    agent_exclude = [
     "bot", "slurp", "crawler", "spider", "curl", "facebook", "fetch", "python"
    ]
    country_lookups = {}
    city_lookups = {}
    signer = Signer()

    def middleware(request):
        track = True
        if any(re.search(p, request.path) for p in path_exclude): track = False
        if track: track = request.META["HTTP_HOST"] not in host_exclude
        if track: track = not any(a in request.META["HTTP_USER_AGENT"].lower() for a in agent_exclude)

        if track:
            ip = ip_from_request(request)
            Visit.objects.create(
             datetime=datetime.utcnow(),
             path=request.path,
             ip_hash=signer.sign(ip).split(":")[1],
             referer=request.META.get("HTTP_REFERER"),
             country=ip_location_lookup(ip, "country_name", country_lookups),
             city=ip_location_lookup(ip, "city", city_lookups),
             agent=request.META.get("HTTP_USER_AGENT")
            )


        response = get_response(request)
        return response
    return middleware

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

def ip_from_request(request):
    ip = None
    for attempt in IP_TRY:
        possible = request.META.get(attempt)
        if possible:
            ip = possible
            break
    return ip



def ip_location_lookup(ip, kind, lookup):
    try:
        return lookup[ip]
    except:
        g = GeoIP2()
        try:
            attr = {"country_name": g.country, "city": g.city}[kind](ip)[kind]
        except: attr = "Unknown"
        lookup[ip] = attr
        return attr
