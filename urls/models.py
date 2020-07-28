from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=255)
    link = models.CharField(max_length=15, null=True, blank=True)
