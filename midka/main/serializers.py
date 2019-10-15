from rest_framework import serializers
from main.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile', 'password')

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = MainUser.objects.create_user(**validated_data)
        profile = Profile.objects.create(user=user, **profile)
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_size(self, value):
        if value < 19 or value > 51:
            raise serializers.ValidationError('Size of product must be in range 20-50')
        return value


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_approximate_duration(self, value):
        if value < 0:
            raise serializers.ValidationError('approximate_duration must be positive')
        return value
