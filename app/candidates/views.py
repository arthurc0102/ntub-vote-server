from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.elections.permissions import IsVoteTimeEndPermission

from django.db.models import Count

from .models import Candidate
from .serializers import CandidateSerializer, CandidateWithCountSerializer


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidate.objects.select_related('pool').all()
    serializer_class = CandidateSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'result':
            return queryset.annotate(vote_count=Count('vote'))

        return queryset

    def get_serializer_class(self):
        if self.action == 'result':
            return CandidateWithCountSerializer

        return super().get_serializer_class()

    @action(['GET'], False, permission_classes=[IsVoteTimeEndPermission])
    def result(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
