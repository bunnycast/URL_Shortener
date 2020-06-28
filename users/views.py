import json

from django.http import HttpResponse
from django.views import View
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class CreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            email=data['email'],
            password=data['password'],
        )

        if User.objects.filter(email=data['email']).exists() == True:
            return HttpResponse({"message : 이미 존재하는 email 입니다."}, status=401)
        else:
            User.objects.create(email=data['email'], password=data['password'])
            return HttpResponse("meassage : 가입되었습니다.", status=200)


class LoginView(View):
    def post(self, request):
        self.request.body['email'] = form.data.get('email')

        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del (request.session['user'])

    return redirect('/')

