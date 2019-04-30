from django.core.exceptions import ValidationError

from rest_framework import serializers

from app.candidates.serializers import PoolCandidateSerializer

from .models import Pool, Vote, Time


class PoolSerializer(serializers.ModelSerializer):
    voted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'voted')

    def get_voted(self, obj):
        std_no = self.context['request'].user.std_no
        for c in obj.candidates.all():
            # NOTE: 這邊沒用 values_list 是為了不讓 Django 再去撈 DB
            if std_no in [v.std_no for v in c.vote_set.all()]:
                return True

        return False


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
        user = self.context['request'].user
        data['std_no'] = user.std_no
        departments = data['candidate'] \
            .pool \
            .departments \
            .values_list('name', flat=True)

        if user.dept_print not in departments:
            raise serializers.ValidationError(
                'You can\'t vote to this candidate.',
            )

        try:
            Vote(**data).full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('start_at', 'end_at', 'is_start', 'is_end', 'is_vote_time')
