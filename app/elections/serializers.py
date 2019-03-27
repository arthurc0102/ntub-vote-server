from rest_framework import serializers

from app.candidates.serializers import PoolCandidateSerializer

from .models import Pool


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = ('id', 'name')


class PoolAndCandidateSerializer(serializers.ModelSerializer):
    candidate_set = PoolCandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'candidate_set')
