from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from app.candidates.serializers import PoolCandidateSerializer

from .models import Pool, Vote


class PoolSerializer(serializers.ModelSerializer):
    voted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'voted')

    def get_voted(self, obj):
        votes = Vote.objects.filter(
            candidate__pool=obj,
            std_no=self.context['request'].user.std_no
        )

        return len(votes) > 0


class PoolAndCandidateSerializer(serializers.ModelSerializer):
    candidates = PoolCandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'candidates')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('candidate', 'is_agree')

    def validate(self, data):
        data['std_no'] = self.context['request'].user.std_no

        try:
            Vote(**data).full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data
