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
    model = User
    fields = ('username', 'email', 'date_joined','password','profile',)
    read_only_fields = ('profile',)

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    profile = Profile.objects.create(user=user)
    return user


class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Department
    fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
  author = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Report
    fields = '__all__'
    read_only_fields = ('date_from', 'author',)


class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'
    read_only_fields = ('created_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ('created_date', 'author','post',)
