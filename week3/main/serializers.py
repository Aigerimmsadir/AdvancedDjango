from rest_framework import serializers
from main.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)
    tasks_count = serializers.IntegerField(default=0)

    class Meta:
        model = Project
        fields = ('id', 'name', 'descr', 'creator_name', 'creator_id', 'tasks_count')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class BlockSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    name = serializers.CharField()
    block_type = serializers.IntegerField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = '__all__'

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''
