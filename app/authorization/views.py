from app.school.services import get_student_info

from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action
from rest_framework.response import Response

from . import services
from .serializers import TokenSerializer


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    permission_classes = []

    @action(['POST'], False)
    def token(self, request):
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
