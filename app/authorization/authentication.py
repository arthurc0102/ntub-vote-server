from django.contrib.auth import get_user_model

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)

from . import services


User = get_user_model()


class JWTVerifyAuthentication(BaseAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'bearer' or len(auth) != 2:
            return None

        token = auth[1].decode(HTTP_HEADER_ENCODING)

        try:
            payload = services.verify_jwt(token)
        except Exception:
            return None

        user = User()
        user.token = token
        user.username = '{std_no}-{std_name}'.format_map(payload)
        [setattr(user, k, v) for k, v in payload.items()]
        return user, None

    def authenticate_header(self, request):
        return f'Bearer realm="{self.www_authenticate_realm}"'
