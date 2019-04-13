from app.school.services import get_student_info

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import services
from .serializers import TokenSerializer


@api_view(['POST'])
@permission_classes([])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = services.check_token(serializer.data['token'])
    student_info = get_student_info(email.split('@')[0])
    token = services.create_jwt(student_info)
    return Response({'token': token})


@api_view(['GET'])
def verify(request):
    return Response({'token': request.user.token})


@api_view(['POST'])
@permission_classes([])
def refresh(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = services.refresh_jwt(serializer.data['token'])
    return Response({'token': token})
