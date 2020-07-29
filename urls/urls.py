from rest_framework.routers import SimpleRouter

from urls.views import UrlViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'urls', UrlViewSet)

urlpatterns = router.urls
