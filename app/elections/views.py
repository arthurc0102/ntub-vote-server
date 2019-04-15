from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.settings import api_settings
from rest_framework.response import Response

from .models import Pool, Vote, Time
from .permissions import IsVoteTimePermission
from .serializers import (
    PoolSerializer,
    PoolAndCandidateSerializer,
    VoteSerializer,
    TimeSerializer,
)


class PoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsVoteTimePermission,
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PoolAndCandidateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        if self.action not in ['list', 'retrieve']:
            return super().get_queryset()

        return Pool.objects.filter(
            departments__name=self.request.user.dept_print,
        )


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsVoteTimePermission,
    ]


class TimeViewSet(viewsets.GenericViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    permission_classes = []

    def list(self, request):
        time = Time.objects.first()
        serializer = self.get_serializer(time)
        return Response(serializer.data)
