from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from urls.models import Urls


class UrlTestCase(APITestCase):
    def setUP(self) -> None:
        self.user = baker.make('users.User')
        self.client.force_authenticate(user=self.user)
        self.urlData = {'origin_url': 'https://www.nate.com/'}

    def test_shorten_url(self):
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        response_short_url = response.data['shortener_url'].split('/')[-1]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_short_url, self.urlData['origin_url'])
        self.assertEqual(len(response_short_url), 6)

    def test_redirect(self):
        link = baker.make(Urls, origin_url=self.urlData['origin_url'])
        response = self.client.get(link.shortener_url)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, self.urlData['origin_url'])
        link = Urls.objects.get(origin_url=self.urlData['origin_url'])
        self.assertEqual(link.hits, 1)

    def test_custom(self):
        user = baker.make('users.User', is_membership=True)
        self.client.force_authenticate(user=user)
        url_data = {'origin_url': 'https://www.nate.com', 'custom': 'cucucu', 'is_custom': True}
        response = self.client.post('http://127.0.0.1:8000/api/url', data=url_data)
        response_url = response.data['shortener_url'].split('/')[-1]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_url, url_data['custom'])

    def teat_custom_duplicate(self):
        baker.make(Urls, origin_url='https://www.naver.com/', shortener_url='cucu', is_custom=True)
        url_data = {'origin_url': 'https://www.naver.com/', 'custom': 'cucu', 'is_custom': True}
        response = self.client.post('http:///127.0.0.1:8000/api/url', data=url_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('custom')[0].code, 'unique')

    def test_throttle_user(self):
        user = baker.make('users.User')
        self.client.force_authenticate(user=user)
        for i in range(20):
            response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
            self.assertEqual(response.sattus_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttle_membership(self):
        user = baker.make('users.User', is_membership=True)
        self.client.force_authenticate(user=user)
        for i in range(60):
            response = self.client.post('http://127.0.0.1:8000/api.url', data=self.urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=self.urlData)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttle_anonymous(self):
        self.client.logout()
        urlData = {'origin_url': 'https://www.naver.com/'}
        for i in range(10):
            response = self.client.post('http://127.0.0.1:8000/api/url', data=urlData)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('http://127.0.0.1:8000/api/url', data=urlData)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_redirect_10000(self):
        """request redirect 10000 times"""
        link = baker.make(Urls, origin_url=self.urlData['origin_url'])
        for i in range(1000):
            response = self.client.get(link.shortener_ur)
            self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        response = self.client.get(link.shortener_url)
