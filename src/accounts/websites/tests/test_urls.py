from dataclasses import dataclass

from django.urls import include, path
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from users.models import User
from ..models import Website


@dataclass
class WebsiteData:
    user: str
    name: str
    url: str
    description: str


class WebsitesUrlsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/v1/accounts/', include('websites.api.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='Тестовое имя',
            email='example@mail.com',
            password='password@mail.com',
        )

    def setUp(self):
        websites = [
            Website(
                user=WebsitesUrlsTests.user,
                name=f'Website name {i}',
                url=f'website.fake/{i}/',
                description=f'Test description {i}'
            ) for i in range(1, 13 + 1)
        ]
        Website.objects.bulk_create(websites)
        self.number_websites = Website.objects.count()
        self.last_post = Website.objects.latest('created')

    def get_id_last_ten_websites(self) -> int:
        """
        Returns the ID of the first website among the last ten.
        """
        start_last_ten_websites_id: int = self.number_websites % 10

        if (self.number_websites // 10) > 1:
            start_last_ten_websites_id += ((self.number_websites // 10) - 1) * 10

        return start_last_ten_websites_id

    # Guest
    def test_urls_get_websites_guest_user(self):
        url = '/api/v1/accounts/websites/'

        response = self.client.get(
            path=url,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {
                'detail': 'Учетные данные не были предоставлены.'
            }
        )

    def test_urls_get_every_website_guest_user(self):
        for website_id in range(1, self.number_websites + 1):
            url = f'/api/v1/accounts/websites/{website_id}/'

            response = self.client.get(
                path=url,
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(
                response.data,
                {
                    'detail': 'Учетные данные не были предоставлены.'
                }
            )

    # Auth user
    def test_urls_get_websites_user(self):
        url = '/api/v1/accounts/websites/'

        self.client.force_authenticate(user=WebsitesUrlsTests.user)
        response = self.client.get(
            path=url,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('results'))

        results = response.data['results']

        first_result_website_id = self.get_id_last_ten_websites()
        i: int = 0
        for website_id in range(self.number_websites, first_result_website_id, -1):
            data_values_expect_values = {
                results[i]['user']: int(WebsitesUrlsTests.user.id),
                results[i]['name']: f'Website name {website_id}',
                results[i]['url']: f'website.fake/{website_id}/',
                results[i]['description']: f'Test description {website_id}'
            }
            i += 1
            for value, expected in data_values_expect_values.items():
                with self.subTest(expected=expected):
                    self.assertEqual(value, expected)

    def test_urls_get_every_website_user(self):
        self.client.force_authenticate(user=WebsitesUrlsTests.user)

        for website_id in range(1, self.number_websites + 1):
            url = f'/api/v1/accounts/websites/{website_id}/'

            response = self.client.get(
                path=url,
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data_values_expect_values = {
                response.data['user']: int(WebsitesUrlsTests.user.id),
                response.data['name']: f'Website name {website_id}',
                response.data['url']: f'website.fake/{website_id}/',
                response.data['description']: f'Test description {website_id}'
            }
            for value, expected in data_values_expect_values.items():
                with self.subTest(expected=expected):
                    self.assertEqual(value, expected)
