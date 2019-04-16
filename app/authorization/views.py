from app.school.services import get_student_info

from config.components.auth import CAN_USE_LOGIN_ACTION

from rest_framework import viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from . import services
from .serializers import TokenSerializer, LoginSerializer


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer

        return super().get_serializer_class()

    @action(['POST'], False)
    def token(self, request):
        """
        Get JWT with google access token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = services.check_token(serializer.data['token'])
        student_info = get_student_info(email.split('@')[0])
        token = services.create_jwt(student_info)
        return Response({'token': token})

    @action(['POST'], False)
    def verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.verify_jwt(serializer.data['token'])
        except Exception:
            raise AuthenticationFailed('Token is invalid or expired.')

        return Response({'token': serializer.data['token']})

    @action(['POST'], False)
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = services.refresh_jwt(serializer.data['token'])
        return Response({'token': token})

    @action(
        ['POST'], False,
        authentication_classes=[
            BasicAuthentication,
            SessionAuthentication,
        ],
        permission_classes=[IsAdminUser]
    )
    def login(self, request):
        """
        Get JWT without google login, just for developing.
        """
        if not CAN_USE_LOGIN_ACTION:
            raise PermissionDenied()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_info = get_student_info(serializer.data['std_no'])
        token = services.create_jwt(student_info, serializer.data['minutes'])
        return Response({'token': token})
