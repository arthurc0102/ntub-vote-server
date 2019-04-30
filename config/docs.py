from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


config = {
    'title': 'NTUB Vote API',
    'authentication_classes': [SessionAuthentication],
    'permission_classes': [IsAdminUser],
}
