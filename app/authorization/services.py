import re
import requests

from rest_framework.exceptions import AuthenticationFailed

from config.components.api import (
    GOOGLE_AUTH_API_URL,
    GOOGLE_AUTH_VALID_HD,
    NTUB_API_URL,
    NTUB_API_HEADERS,
)


def check_token(token):
    res = requests.get(GOOGLE_AUTH_API_URL, {
        'alt': 'json',
        'access_token': token,
    })

    if not res.ok:
        raise AuthenticationFailed()

    user_info = res.json()
    if user_info['hd'] not in GOOGLE_AUTH_VALID_HD:
        raise AuthenticationFailed()

    return user_info['email']


def get_student_info(std_no):
    res = requests.post(NTUB_API_URL, std_no, headers=NTUB_API_HEADERS)
    if not res.ok:
        raise AuthenticationFailed()

    data = {}
    for k, v in res.json()[0].items():
        key = k.lower()
        key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        data[key] = v

    return data
