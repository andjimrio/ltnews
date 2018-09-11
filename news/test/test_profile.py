from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from news.models import User, Profile


class ProfileTestCase(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'abc123..'
        self.user = User.objects.create(username=self.username, password=self.password)
        Profile.objects.create(user=self.user)

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_detail_get_ok(self):
        response = self.client.get('/profile/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_detail_put_ok(self):
        self.assertEqual("", self.__get_profile().image)

        image_new = "https://assets.pernod-ricard.com/uk/media_images/test.jpg"
        response = self.client.put('/profile/', {"image": image_new})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(image_new, Profile.objects.get(user__username=self.username).image)

    def test_detail_put_ko_json(self):
        response = self.client.put('/profile/', {"image": "not_url"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stats_get_ok_read(self):
        response = self.client.get('/profile/stats/read/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_stats_get_ok_like(self):
        response = self.client.get('/profile/stats/like/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_stats_get_ko_param(self):
        response = self.client.get('/profile/stats/param/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(b"[]", response.content)

    def __get_profile(self):
        return Profile.objects.get(user__username=self.username)
