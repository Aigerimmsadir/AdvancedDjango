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
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectMemberFullSerializer
        return ProjectMemberSerializer

    @action(methods=['GET', 'POST'], detail=True)
    def members(self, request, pk):
        if request.method == 'GET':
            project = Project.objects.get(id=pk)
            projectmembers = project.project_members.all()
            serializer = ProjectMemberSerializer(projectmembers, many=True)
            return Response(serializer.data)
        else:
            project = Project.objects.get(id=pk)
            user = self.request.user
            projectmember = ProjectMember(project=project, user=user)
            projectmember.save()
            serializer = ProjectMemberSerializer(projectmember)
            return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def sort_by_user_last_name(self, request):
        projectmembers = ProjectMember.members.sort_by_user_last_name()
        serializer = ProjectMemberFullSerializer(projectmembers, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def members_of_my_projects(self, request):
        projectmembers = ProjectMember.members.members_of_my_projects(self.request.user)
        serializer = ProjectMemberFullSerializer(projectmembers, many=True)
        return Response(serializer.data)
    @action(methods=['GET'], detail=False)
    def members_of_my_projects_ordered(self, request):
        projectmembers = ProjectMember.members.members_of_my_projects_ordered(self.request.user)
        serializer = ProjectMemberFullSerializer(projectmembers, many=True)
        return Response(serializer.data)

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
        projects = Project.projects.my_projects(request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def more_than_2_members(self, request):
        projects = Project.projects.more_than_2_members()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskFullSerializer
        return TaskShortSerializer

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"{self.request.user} created task: {serializer.data.get('name')}")

    @action(methods=['GET'], detail=False)
    def for_me(self, request):
        tasks = Task.tasks.tasks_for_me(self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def my_tasks(self, request):
        tasks = Task.tasks.my_tasks(self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def tasks_to_execute(self, request):
        tasks = Task.tasks.tasks_to_execute(self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def tasks_with_media(self, request):
        tasks = Task.tasks.tasks_with_media()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskCommentFullSerializer
        return TaskCommentSerializer

    @action(methods=['GET'], detail=True)
    def comments_of_task(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskCommentSerializer(task.comments, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def comments_to_my_tasks(self, request):
        tasks = TaskComment.comments.comments_to_my_tasks(self.request.user)
        serializer = TaskCommentSerializer(tasks, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MainUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializerFull
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
