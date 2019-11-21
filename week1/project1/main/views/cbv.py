from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryAdvertisements(APIView):
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('name', 'description')

    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        advertisements = Advertisement.objects.filter(category=category)
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        category = self.get_object(pk)
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category, owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvertisementDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        advertisement = self.get_object(pk)

        serializer = AdvertisementSerializer(advertisement)
        return Response(serializer.data)

    def put(self, request, pk):
        advertisement = self.get_object(pk)
        serializer = AdvertisementSerializer(instance=advertisement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        advertisement = self.get_object(pk)
        advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserComments(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        advertisement = self.get_object(pk)
        comments = Comment.objects.filter(advertisement=advertisement, owner=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class Comments(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        advertisement = self.get_object(pk)
        comments = Comment.objects.filter(advertisement=advertisement)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        advertisement = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(advertisement=advertisement, owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
