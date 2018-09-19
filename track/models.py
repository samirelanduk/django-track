
from django.db import models

class Visit(models.Model):

    class Meta:
        ordering = ["-datetime"]

    datetime = models.DateTimeField()
    path = models.CharField(max_length=256, blank=True, null=True)
    IP = models.CharField(max_length=64, blank=True, null=True)
    referer = models.CharField(max_length=256, blank=True, null=True)
