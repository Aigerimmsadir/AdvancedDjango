from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.permissions import *
from main.serializers import UserSerializer
from main.models import MainUser


class RegisterUserViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer


class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsSuperAdminPermission,)
    queryset = MainUser.objects.all()

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
