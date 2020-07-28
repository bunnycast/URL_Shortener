from rest_framework import serializers

from urls.models import Url


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('id', 'url', 'link')
