from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import *



class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = MainUser.objects.all()

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
