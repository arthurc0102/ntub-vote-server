from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Pool
from .serializers import PoolSerializer, PoolAndCandidateSerializer


class PoolViewSet(ReadOnlyModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PoolAndCandidateSerializer

        return super().get_serializer_class()
