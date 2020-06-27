from django.contrib.auth.models import User
from django.db import models


class Urls(models.Model):
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE, related_name='urls')
    origin_urls = models.URLField()
    tiny_urls = models.URLField()
