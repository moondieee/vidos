from dataclasses import dataclass

from django.urls import include, path
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.authtoken.models import Token

from ..api.serializers import UserGETSerializer
from ..models import User


@dataclass
class UserCredentials:
    username: str
    email: str
    password: str


class UsersUrlsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/v1/accounts/', include('users.api.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_credentials = UserCredentials(
            username='Тестовое имя',
            email='example@mail.com',
            password='password@mail.com'
        )

        cls.user = User.objects.create_user(
            username=cls.user_credentials.username,
            email=cls.user_credentials.email,
            password=cls.user_credentials.password
        )

    def setUp(self):
        self.token: str = str(
            Token.objects.create(
                user=UsersUrlsTests.user
            )
        )

    # Authentication
    def test_urls_token_login(self):
        url = '/api/v1/accounts/token/login/'
        data = {
            'email': UsersUrlsTests.user_credentials.email,
            'password': UsersUrlsTests.user_credentials.password
        }

        response = self.client.post(
            path=url,
            format='json',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            {
                'auth_token': self.token
            }
        )

    def test_urls_token_logout(self):
        self.client.login(
            email=UsersUrlsTests.user_credentials.email,
            password=UsersUrlsTests.user_credentials.password
        )

        url = '/api/v1/accounts/token/logout/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Token.objects.filter(
                user_id=UsersUrlsTests.user.id,
                key=self.token
            ).exists()
        )

    # Users
    def test_get_own_user_data(self):
        logout_url = '/api/v1/accounts/users/me/'
        response = self.client.get(
            path=logout_url,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        user_data: dict = UserGETSerializer(UsersUrlsTests.user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_data)
