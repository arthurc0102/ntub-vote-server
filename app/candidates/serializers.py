from rest_framework import serializers

from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    pool = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateWithCountSerializer(serializers.ModelSerializer):
    pool = serializers.SlugRelatedField('name', read_only=True)
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class PoolCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ('pool',)
