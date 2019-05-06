from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.settings import api_settings
from rest_framework.response import Response

from django.db.models import Count, Q

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
        queryset = super().get_queryset()

        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(
                Q(departments__name=self.request.user.dept_print) |
                Q(groups__student__std_no=self.request.user.std_no)
            )

        if self.action == 'list':
            queryset = queryset \
                .prefetch_related('candidates__vote_set') \
                .annotate(candidate_count=Count('candidates')) \
                .filter(candidate_count__gt=0)

        return queryset


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
