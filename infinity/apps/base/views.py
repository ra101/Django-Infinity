import requests

from django.http import HttpResponse, HttpResponseServerError

from markdown import markdown


def hello_world(*args, **kwargs):
    return HttpResponse("Hello World")

def readme(*args, **kwargs):
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/ra101/Django-Infinity/core/README.md"
        )
        return HttpResponse(markdown(response.text))
    except Exception:
        return HttpResponseServerError()
