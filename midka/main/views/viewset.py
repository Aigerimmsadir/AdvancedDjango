from rest_framework import viewsets
from rest_framework import mixins
from main.permissions import *
from main.models import *
from main.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminPermission,)



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminPermission,)


class ProductListViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ServiceListViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)


class ProductModifyViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminPermission,)


class ServiceModifyViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminPermission,)

