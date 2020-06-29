from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
