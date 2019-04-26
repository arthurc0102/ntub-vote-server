from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


config = {
    'title': 'NTUB Vote API',
    'public': False,
    'authentication_classes': [SessionAuthentication],
    'permission_classes': [IsAdminUser],
}
