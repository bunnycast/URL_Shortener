import string
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

words = string.ascii_letters + string.digits


class Urls(models.Model):
    origin_url = models.URLField()
    shorten_url = models.CharField(max_length=200, unique=True)
    hits = models.IntegerField(default=0)
    owner = models.ForeignKey('users.User', related_name='urls', on_delete=models.CASCADE, null=True)
    is_custom = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (not self.hits) and (not self.is_custom):
            self.shortenUrl = self.make_short_uuid()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def shortenUrl(self):
        return f"http://127.0.0.1:8000/api/urls/{self.shorten_url}"

    @shortenUrl.setter
    def shortenUrl(self, val):
        self.shorten_url = val

    def make_short_uuid(self):
        for i in range(20):
            u = uuid4().hex[:6]
            if not Urls.objects.filter(shorten_url=u).exists():
                return u
