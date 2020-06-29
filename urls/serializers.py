import string

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from urls.models import Urls

words = string.ascii_letters + string.digits


class GetUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = ('origin_url', 'shorten_url', 'hits', 'owner',)
        read_only_fields = fields


class CreateUrlSerializer(serializers.ModelSerializer):
    custom = serializers.CharField(max_length=200, required=False, source='shorten_url', validators=[
        UniqueValidator(queryset=Urls.objects.all(), message="이미 존재하는 URL입니다. 다시 입력해주세요.")])

    class Meta:
        model = Urls
        fields = ('origin_url', 'shorten_url', 'hits', 'custom', 'is_custom',)
        read_only_fields = ('shorten_url', )
