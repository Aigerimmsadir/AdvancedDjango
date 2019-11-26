from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import logging
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from main.models import *
from main.serializers import *
from rest_framework.views import APIView
logger = logging.getLogger(__name__)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleFullSerializer
        return ArticleSerializer

    @action(methods=['GET', 'POST'], detail=False)
    def favorite(self, request):
        if request.method == 'GET':
            fav_articles = request.user.favorite_articles.all()
            articles = Article.objects.filter(id__in=fav_articles.values('article_id'))
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
        else:
            print(request.data)
            article_ids = request.data['article_ids']
            for i in article_ids:
                print(i)
                try:
                    article = Article.objects.get(id=i)
                    FavoriteArticle.objects.create(article=article, user=request.user)
                except:
                    raise Exception('not such article')
            fav_articles = request.user.favorite_articles.all()
            articles = Article.objects.filter(id__in=fav_articles.values('article_id'))
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

