import requests

from markdown import markdown
from django.http import HttpResponse, HttpResponseServerError

from .constants import Readme


def hello_world(*args, **kwargs):
    return HttpResponse("Hello World")

def readme(*args, **kwargs):
    try:
        response = requests.get(Readme.URL)
        return HttpResponse(markdown(response.text))
    except Exception:
        return HttpResponseServerError()
