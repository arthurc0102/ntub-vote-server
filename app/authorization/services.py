import jwt
import requests

from config.components.api import GOOGLE_AUTH_API_URL, GOOGLE_AUTH_VALID_HD
from config.components.common import SECRET_KEY
from config.components.jwt import (
    JWT_ALGORITHM,
    ACCESS_LIFETIME,
    REFRESH_LIFETIME,
)

from calendar import timegm

from datetime import datetime, timedelta

from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


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


def create_jwt(payload, access=ACCESS_LIFETIME, refresh=REFRESH_LIFETIME):
    assert type(payload) is dict, 'Payload type error.'

    utc = datetime.utcnow()
    refresh_exp = timegm((utc + timedelta(minutes=refresh)).utctimetuple())
    payload.update({
        'iat': utc,
        'exp': utc + timedelta(minutes=access),
        'refresh_exp': refresh_exp,
    })

    return jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)


def verify_jwt(token, verify=True):
    return jwt.decode(token, SECRET_KEY, verify, [JWT_ALGORITHM])


def refresh_jwt(token):
    now = timegm((datetime.utcnow()).utctimetuple())

    try:
        payload = verify_jwt(token)
    except jwt.ExpiredSignatureError:
        payload = verify_jwt(token, False)
    except Exception:
        raise PermissionDenied('Token is invalid.')

    refresh_exp = payload['refresh_exp']

    try:
        refresh_exp = int(refresh_exp)
    except Exception:
        raise PermissionDenied('Token is invalid.')

    if refresh_exp < now:
        raise PermissionDenied('Token is expired to refresh.')

    return create_jwt(payload)
