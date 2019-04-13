import jwt
import re
import requests

from config.components.common import SECRET_KEY
from config.components.jwt import JWT_ALGORITHM
from config.components.api import (
    GOOGLE_AUTH_API_URL,
    GOOGLE_AUTH_VALID_HD,
    NTUB_API_URL,
    NTUB_API_HEADERS,
)

from datetime import datetime, timedelta

from rest_framework.exceptions import AuthenticationFailed


INFO_KEYS = ['std_no', 'std_name', 'dept_print']


def check_token(token):
    res = requests.get(GOOGLE_AUTH_API_URL, {
        'alt': 'json',
        'access_token': token,
    })

    if not res.ok:
        raise AuthenticationFailed()

    user_info = res.json()
    if user_info.get('hd') not in GOOGLE_AUTH_VALID_HD:
        raise AuthenticationFailed()

    if not user_info.get('email'):
        raise AuthenticationFailed()

    return user_info['email']


def get_student_info(std_no, keys=INFO_KEYS):
    res = requests.post(NTUB_API_URL, std_no, headers=NTUB_API_HEADERS)
    if not res.ok or not res.json():
        raise AuthenticationFailed()

    data = {}
    for k, v in res.json()[0].items():
        key = k.replace('_', '')
        key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        data[key] = v

    if data.get('status') != '在學':
        raise AuthenticationFailed()

    return {k: v for k, v in data.items() if k in keys}


def create_jwt(payload):
    assert type(payload) is dict, 'Payload type error.'

    utc = datetime.utcnow()
    payload.update({
        'iat': utc,
        'exp': utc + timedelta(minutes=10),
    })

    return jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)


def verify_jwt(token, verify=True):
    return jwt.decode(token, SECRET_KEY, verify, [JWT_ALGORITHM])


def refresh_jwt(token):
    try:
        payload = verify_jwt(token)
    except Exception:
        raise AuthenticationFailed()

    return create_jwt(payload)
