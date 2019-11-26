from django.urls import path
from .views import *

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

urlpatterns = [
    path('login/', obtain_jwt_token),
]

router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='auth')
urlpatterns += router.urls
