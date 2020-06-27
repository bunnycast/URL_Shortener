from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from users.views import CreateView

urlpatterns = [
    path('signup/', csrf_exempt(CreateView.as_view())),
    # path('users/', listView.as_view()),
]
