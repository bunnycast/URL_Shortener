import string

from django.http import HttpResponsePermanentRedirect
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from core import throttles
from urls.models import Urls
from urls.serializers import CreateUrlSerializer, GetUrlSerializer

words = string.ascii_letters + string.digits


class ShortenerViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
        queryset = Urls.objects.all()
        serializer_class = CreateUrlSerializer

        def get_permission(self):
            if self.action == 'create':
                return [AllowAny()]
            return super().get_permissions()

        def get_throttles(self):
            if self.action == 'create':
                if self.request.user.is_anonymous:
                    return [throttles.AnonThrottle()]
                elif self.request.user.is_membership:
                    return [throttles.MembershipThrottle()]
                else:
                    return [throttles.UserThrottle]
            else:
                return super().get_throttles()

        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)

        def perform_create(self, serializer):
            if self.request.user.is_anonymous:
                serializer.save()
            else:
                serializer.save(owner=self.request.user)

        def filter_queryset(self, queryset):
            if self.request.user.is_anonymous:
                return queryset.filter(pk=-1)
            elif self.request.user.is_membership:
                return queryset.filter(owner=self.request.user)
            else:
                return queryset.filter(owner=self.request.user)


class UrlViewSet(mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Urls.objects.all()
    serializer_class = GetUrlSerializer
    lookup_field = 'shortener_url'
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        '''
        GET /api/url/~ 요청시  realUrl 리다이렉트
        + hits
        '''
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return HttpResponsePermanentRedirect(redirect_to=serializer.data['original_url'])
