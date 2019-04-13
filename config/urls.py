"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.authorization.views import token, verify, refresh
from app.candidates.views import CandidateViewSet
from app.elections.views import PoolViewSet

from config.settings import DEBUG
from config.components.static import MEDIA_ROOT, MEDIA_URL

from rest_framework import routers


route = routers.SimpleRouter()
route.trailing_slash = ''
route.register('candidates', CandidateViewSet)
route.register('vote-pools', PoolViewSet)


urlpatterns = [
    path('', include(route.urls)),
    path('auth/token', token, name='auth-token'),
    path('auth/token/verify', verify, name='auth-verify'),
    path('auth/token/refresh', refresh, name='auth-refresh'),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
