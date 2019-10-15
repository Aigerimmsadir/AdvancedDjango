from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from main.views import *

from main.views import *
urlpatterns = [
    path('login/', obtain_jwt_token),
]


router = DefaultRouter()
router.register('users', UserViewSet, base_name='main')
router.register('register_v', RegisterUserViewSet, base_name='main')
router.register('products', ProductViewSet, base_name='main')
router.register('product_list', ProductListViewSet, base_name='main')
router.register('product_modify', ProductModifyViewSet, base_name='main')
router.register('service_modify', ServiceModifyViewSet, base_name='main')
router.register('service_list', ServiceListViewSet, base_name='main')
router.register('services', ServiceViewSet, base_name='main')
urlpatterns += router.urls