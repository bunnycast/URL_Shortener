from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class UrlViewSetTestCase(APITestCase):
    def setUp(self):
        pass

    def test_url_shorten(self):
        data = {
            'url': 'www.google.com',
        }
        response = self.client.post('/api/urls/shorten', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['url'], data['url'])

        self.fail()
