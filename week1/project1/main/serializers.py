from rest_framework import serializers
from main.models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField()

    class Meta:
        model = Category
        fields = '__all__'


class AdvertisementSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    image = serializers.CharField()

    def create(self, validated_data):
        advertisement = Advertisement(**validated_data)
        advertisement.save()
        return advertisement

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    owner = UserSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.save()
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
