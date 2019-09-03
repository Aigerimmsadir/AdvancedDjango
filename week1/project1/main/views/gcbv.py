from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.filters import *
from main.models import *
from main.serializers import *
from rest_framework import filters

class AdvertisementList(generics.ListCreateAPIView):
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class= AdvertisementFilter
    def get_queryset(self):
        try:
            category = Category.objects.get(id=self.kwargs.get('pk'))
            print(category)
        except Category.DoesNotExist:
            raise Http404
        queryset = Advertisement.objects.filter(category=category)

        return queryset

    def perform_create(self, serializer):
        try:
            category = Category.objects.get(id=self.kwargs.get('pk'))
            print(category)
        except Category.DoesNotExist:
            raise Http404
        serializer.save(owner=self.request.user,category=category) 