from rest_framework import viewsets

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidate.objects.select_related('pool').all()
    serializer_class = CandidateSerializer
    permission_classes = []
