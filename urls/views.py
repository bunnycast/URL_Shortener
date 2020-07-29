import time

from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from urls.models import Url
from urls.serializers import UrlSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    @action(methods=['POST'], detail=False)
    def shorten(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)

    # use caching
    def retrieve(self, request, *args, **kwargs):
        key = kwargs['pk']
        instance = cache.get(key)

        if not instance:

            time.sleep(3)
            print('sleep')

            instance = self.get_object()
            cache.set(key, instance, 60)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

