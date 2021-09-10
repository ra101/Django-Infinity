from uuid import uuid4

from django.urls import reverse
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from constance import config as live_settings


@tag('home')
class HomeTests(APITestCase):
    """
    Test Case(s) for /home.html
    """

    request = lambda self: self.client.get(
        reverse('home')
    )

    def test_successful(self):
        """Successfully ping at the right address"""

        response = self.request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'Hello World')


@tag('live-url-demo')
class LiveDemoTests(APITestCase):
    """
    Test Case(s) for /live_settings/<str:live_url_endpoint>/
    """

    request = lambda self, kwargs: self.client.get(
        reverse('live-url-demo', kwargs=kwargs)
    )

    def test_successful(self):
        """Successfully ping at the right address"""

        # Back-up original keys
        original_live_key = live_settings.LIVE_KEY
        original_live_value = live_settings.LIVE_VALUE
        original_live_url_endpoint = live_settings.LIVE_URL_ENDPOINT

        # Update Key
        live_key = live_settings.LIVE_KEY = f"{uuid4()}"
        live_value = live_settings.LIVE_VALUE = f"{uuid4()}"
        live_url_endpoint = live_settings.LIVE_URL_ENDPOINT = f"{uuid4()}"

        response = self.request(kwargs={"live_url_endpoint": live_url_endpoint})

        # Restore original keys
        live_settings.LIVE_KEY = original_live_key
        live_settings.LIVE_VALUE = original_live_value
        live_settings.LIVE_URL_ENDPOINT = original_live_url_endpoint

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json, {live_key: live_value}
        )

    def test_invalid_url_endpoint(self):
        """If Incorrect <URL param> is sent"""

        response = self.request(kwargs={"live_url_endpoint": f"{uuid4()}"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
