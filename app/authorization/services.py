import jwt
import requests

from config.components.common import SECRET_KEY
from config.components.jwt import JWT_ALGORITHM
from config.components.api import GOOGLE_AUTH_API_URL, GOOGLE_AUTH_VALID_HD

from calendar import timegm

from datetime import datetime, timedelta

from rest_framework.exceptions import AuthenticationFailed


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


def create_jwt(payload, minutes=10):
    assert type(payload) is dict, 'Payload type error.'

    utc = datetime.utcnow()
    refresh_exp = timegm((utc + timedelta(minutes=minutes+10)).utctimetuple())
    payload.update({
        'iat': utc,
        'exp': utc + timedelta(minutes=minutes),
        'refresh_exp': refresh_exp,
    })

    return jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)


def verify_jwt(token, verify=True):
    return jwt.decode(token, SECRET_KEY, verify, [JWT_ALGORITHM])


def refresh_jwt(token):
    payload = verify_jwt(token, False)
    refresh_exp = payload['refresh_exp']
    now = timegm((datetime.utcnow()).utctimetuple())

    if not refresh_exp.isdigit():
        raise AuthenticationFailed('Token is invalid or expired.')

    refresh_exp = int(refresh_exp)

    if refresh_exp < now:
        raise AuthenticationFailed('Token is invalid or expired.')

    return create_jwt(payload)
