from rest_framework import serializers

from .models import Candidate


class PoolCandidateSerializer(serializers.ModelSerializer):
    system = serializers.SlugRelatedField('name', read_only=True)
    department = serializers.SlugRelatedField('name', read_only=True)
    grade = serializers.SlugRelatedField('name', read_only=True)
    klass = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Candidate
        exclude = ('pool',)
