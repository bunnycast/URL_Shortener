from rest_framework.serializers import ModelSerializer

from urls.models import Urls


class UrlsSerializer(ModelSerializer):
    class Meta:
        model = Urls
        field = ('user', 'origin_urls', 'tiny_urls',)
