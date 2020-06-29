from rest_framework.serializers import ModelSerializer

from urls.serializers import GetUrlSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    urls = GetUrlSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'urls',)
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
