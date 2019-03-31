from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import services
from .serializers import LoginSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = services.check_token(serializer.data['token'])
    student_info = services.get_student_info(email.split('@')[0])
    return Response(student_info)
