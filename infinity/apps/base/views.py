import requests

from markdown import markdown
from constance import config as live_settings
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .constants import Readme


def hello_world_view(request):
    return HttpResponse("Hello World")

def readme_view(request):
    try:
        response = requests.get(Readme.URL)
        print(response.status_code)
        if 200 <= response.status_code < 300:
            return HttpResponse(markdown(response.text))
        return HttpResponseServerError()
    except Exception:
        return HttpResponseServerError()

@api_view(http_method_names=['GET'])
def live_view(request, live_url_endpoint):
    if live_url_endpoint != live_settings.LIVE_URL_ENDPOINT:
        raise NotFound()
    return Response({
        live_settings.LIVE_KEY: live_settings.LIVE_VALUE
    })
