import requests

from markdown import markdown
from constance import config as live_settings
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.serializers import Serializer, CharField

from .constants import Readme


def hello_world_view(request):
    # for pinger, https://github.com/ra101/pinger
    return HttpResponse("Hello World")


def readme_view(request):
    try:
        response = requests.get(Readme.URL)
        if 200 <= response.status_code < 300:
            return HttpResponse(markdown(response.text))
        return HttpResponseServerError()
    except Exception:
        return HttpResponseServerError()


@api_view(http_method_names=["GET"])
def live_view(request, live_url_endpoint):

    # 404 for incorrent url param
    if live_url_endpoint != live_settings.LIVE_URL_ENDPOINT:
        raise NotFound(
            f"Given URL param <live_url_endpoint:{live_url_endpoint}> "
            "does not match with constance.config.LIVE_URL_ENDPOINT"
        )

    # commenting this part to make a unnecessary dynamic serializer
    # return Response({live_settings.LIVE_KEY: live_settings.LIVE_VALUE})

    # The Highly Unnecessary "Dynamic Serializer"
    # If its is unnecessary, then Why?
    # Because I can :p
    LiveSerializer = type(
        "LiveSerializer", (Serializer,), {live_settings.LIVE_KEY: CharField()}
    )

    serializer = LiveSerializer(data={live_settings.LIVE_KEY: live_settings.LIVE_VALUE})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
