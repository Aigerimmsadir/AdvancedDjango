from rest_framework import serializers
from main.models import *
from django.db import transaction


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
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile')

    def create(self, validated_data):
        with transaction.atomic():
            profile_data = validated_data.pop('profile')
            user = MainUser.objects.create_user(**validated_data)
            Profile.objects.create(user=user, **profile_data)
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


class ProjectMemberSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'creator_id')

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    block_id = serializers.IntegerField(write_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id', 'name', 'order', 'executor', 'creator', 'block_id')

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('name length less than 3')
        return value


class TaskFullSerializer(TaskShortSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer()

    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('descr',)


class TaskCommentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = '__all__'


class TaskDocumentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = TaskDocument
        fields = '__all__'
