from uuid import uuid4

from django.urls import reverse
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase
from constance.test import override_config as override_live_settings

from infinity.constants import LiveDemoInitialConfig


@tag("home")
class HomeTests(APITestCase):
    """
    Test Case(s) for /home.html
    """

    request = lambda self: self.client.get(reverse("home"))

    def test_successful(self):
        """Successfully ping at the right address"""

        response = self.request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"Hello World")


@tag("live-url-demo")
class LiveDemoTests(APITestCase):
    """
    Test Case(s) for /live_settings/<str:live_url_endpoint>/
    """

    request = lambda self, kwargs: self.client.get(
        reverse("live-url-demo", kwargs=kwargs)
    )

    TEST_KEY = str(uuid4())
    TEST_VALUE = str(uuid4())
    TEST_ENDPOINT = str(uuid4())

    def test_default_live_settings(self):
        """Successfully ping at the right address"""

        response = self.request(
            kwargs={"live_url_endpoint": LiveDemoInitialConfig.ENDPOINT}
        )

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json, {LiveDemoInitialConfig.KEY: LiveDemoInitialConfig.VALUE}
        )

    @override_live_settings(
        LIVE_KEY=TEST_KEY, LIVE_VALUE=TEST_VALUE, LIVE_URL_ENDPOINT=TEST_ENDPOINT
    )
    def test_update_live_settings(self):
        """Successfully ping at the right address"""

        response = self.request(kwargs={"live_url_endpoint": self.TEST_ENDPOINT})

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, {self.TEST_KEY: self.TEST_VALUE})

    def test_invalid_url_endpoint(self):
        """If Incorrect <URL param> is sent"""

        response = self.request(kwargs={"live_url_endpoint": str(uuid4())})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
