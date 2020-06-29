from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.permissions import IsUserSelf
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return [AllowAny()]
        elif self.name == 'Login':
            return [AllowAny()]

        if self.action == 'deactivate':
            return [IsUserSelf()]

        return super().get_permissions()

    @action(methods=('post',), detail=False)
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_created(user=user)

    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        return response

    def partiail_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)