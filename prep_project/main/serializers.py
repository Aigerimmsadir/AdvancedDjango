from .models import *
from rest_framework import serializers

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = '__all__'

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user

