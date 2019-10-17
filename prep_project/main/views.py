from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.models import *
from main.serializers import *


class RegisterUserViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserViewSet(
  mixins.ListModelMixin, mixins.RetrieveModelMixin,
  mixins.DestroyModelMixin,
  viewsets.GenericViewSet):
  serializer_class = UserSerializer
  permission_classes = (IsAuthenticated,)
  queryset = User.objects.all()

  @action(methods=['GET'], detail=False)
  def me(self, request):
    serializer = self.get_serializer(request.user)
    return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = (IsAuthenticated,)


class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer
  permission_classes = (IsAuthenticated,)


class DepartmentViewSet(viewsets.ModelViewSet):
  queryset = Department.objects.all()
  serializer_class = DepartmentSerializer
  permission_classes = (IsAuthenticated,)


class CommentList(APIView):
  http_method_names = ['get', 'post']
  permission_classes = (IsAuthenticated,)

  def get_project(self, pk):
    return Post.objects.get(id=pk)

  def get(self, request, pk):
    post = self.get_project(pk)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

  def post(self, request, pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(post_id=pk, author  =request.user)
      return Response(serializer.data)
    return Response(serializer.errors)



class ProfileCreate(APIView):
  http_method_names = ['post']
  permission_classes = (IsAuthenticated,)

  def post(self, request, pk):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user  =request.user)
      return Response(serializer.data)
    return Response(serializer.errors)
