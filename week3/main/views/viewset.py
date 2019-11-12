from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import *
import logging
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from main.models import *
from main.serializers import *

logger = logging.getLogger(__name__)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = (IsAuthenticated,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectFullSerializer
        return ProjectSerializer

    @action(methods=['GET'], detail=False)
    def myprojects(self, request):
        projects = Project.for_user(request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    # serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskFullSerializer
        return TaskShortSerializer

    @action(methods=['GET'], detail=True)
    def blocktasks(self, request, pk):
        block = Block.objects.get(id=pk)
        serializer = TaskSerializer(block.tasks, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        logger.error(f"{self.request.user} created task: {serializer.data.get('name')}")


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskCommentSerializer(task.comments, many=True)
        return Response(serializer.data)
