from rest_framework.serializers import ModelSerializer

from urls.serializers import UrlsSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    urls = UrlsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'urls',)
