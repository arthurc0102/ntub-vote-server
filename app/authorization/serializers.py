from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    std_no = serializers.CharField()
    access = serializers.IntegerField(
        min_value=1,
        max_value=1000000,
        default=30,
    )
    refresh = serializers.IntegerField(
        min_value=1,
        max_value=1000000,
        default=30,
    )
