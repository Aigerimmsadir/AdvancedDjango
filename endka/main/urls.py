from django.urls import path
from main.views import *

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('articles', ArticleViewSet, base_name='main')
urlpatterns += router.urls
