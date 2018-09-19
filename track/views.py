from django.shortcuts import render
from .models import Visit

def analytics(request):
    return render(request, "track/analytics.html", {"visits": Visit.objects.all()})
