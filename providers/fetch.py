from json import loads
from requests import request, HTTPError

from providers.namespace import RecursiveNamespace


def fetch_json(*args, **kwargs):
    response = request(*args, **kwargs)
    response.raise_for_status()

    return loads(response.text, object_hook=lambda d: RecursiveNamespace(**d))
