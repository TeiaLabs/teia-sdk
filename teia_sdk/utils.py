import json
import requests
from httpx import HTTPError
from rich import print

from http_error_schemas.factory import get_error_class


def pjson(obj):
    """Prettify JSON."""
    return json.dumps(obj, indent=4, sort_keys=True)


def ppjson(obj):
    """Pretty print JSON."""
    print(pjson(obj))


def handle_erros(response: requests.Response):
    """Handle HTTP errors."""

    try:
        response.raise_for_status()
    except HTTPError as e:
        exc = get_error_class(response.status_code)
        print(exc(**response.json()))
        exit(1)
