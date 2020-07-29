from django.core.cache import cache
from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=255)
    link = models.CharField(max_length=15, null=True, blank=True)

    # use caching at instance create, update
    def save(self, **kwargs):
        key = self.id
        if key:
            cache.delete(key)

        super().save(**kwargs)

    # use caching at instance delete
    def delete(self, **kwargs):
        key = self.id
        cache.delete(key)

        return super().delete()
