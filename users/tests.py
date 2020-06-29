from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make('users.User', passwrod='1111', username='user')
        self.data = {'username': self.user.username, 'password': '1111'}

    def test_register(self):
        data = {'username': 'user1', 'password': '1111'}
        response = self.client.post('/api/users/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post('/api/users/login', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['token'])

    def test_logout(self):
        # token = baker.make(Token, user=self.user)
        token = Token.objects.get(user_id=self.user.id)
        self.client.force_authenticate(user=self.user, token=token.key)
        response = self.client.get('/api/users/logout')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate(self):
        user = User.objects.get(pk=self.user.id)
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{self.user.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        prev_data = User.objects.get(pk=self.user.id)
        data = {'username': 'new_username', 'password': '1111'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/users/{self.user.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertNotEqual(response.data['username'], prev_data.username)

    def test_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        pass