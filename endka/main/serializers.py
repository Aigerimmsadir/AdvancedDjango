from rest_framework import serializers
from main.models import *
from django.db import transaction
import logging
from auth1.serializers import UserSerializer

logger = logging.getLogger(__name__)


class ArticleSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_name = serializers.SerializerMethodField()
    images_uploaded = serializers.ListField(
        child=serializers.ImageField(), required=False
    )

    class Meta:
        model = Article
        fields = ('id', 'name', 'price', 'creator_name', 'creator', 'city', 'category', 'color', 'images_uploaded')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('price must be positive integer')
        return value

    def create(self, validated_data):
        imgs = validated_data.pop('images_uploaded')
        article = Article(**validated_data)
        article.save()
        for i in imgs:
            img = ArticleImage(image=i, article=article)
            img.save()
        return article


class ArticleFullSerializer(ArticleSerializer):
    creator = UserSerializer(read_only=True)

    # images = serializers.ListField(
    #     child=serializers.IntegerField(), required=False
    # )

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('description', 'images')
