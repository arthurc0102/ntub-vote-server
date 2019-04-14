from rest_framework import viewsets

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = []
