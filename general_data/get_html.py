import requests

from general_data.CONSTANTS import HEADERS


def get_html(url, params=None):
    request = requests.get(url, headers=HEADERS, params=params)
    return request
