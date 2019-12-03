from django.urls import path
from main.views import *

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('logout/', logout),
    path('current/', current),
    path('register/', UserCreate.as_view()),
    path('project_list/', ProjectList.as_view()),
    path('project_list/<int:pk>/', ProjectDetail.as_view()),
    path('task_comments/', TaskCommentList.as_view()),
    path('task_comments/<int:pk>/', TaskCommentDetail.as_view()),
    path('task_documents/', TaskDocumentList.as_view()),
    path('task_documents/<int:pk>/', TaskDocumentDetail.as_view()),
    path('project_list/<int:pk>/blocks/', BlockListAPIView.as_view()),
    path('blocks/<int:pk>/', BlockDetailAPIView.as_view()),
]

router = routers.DefaultRouter()
router.register('project_list/members', ProjectMemberViewSet, base_name='main')
router.register('tasks', TaskViewSet, base_name='main')
router.register('users', UserViewSet, base_name='main')
router.register('projects', ProjectViewSet, base_name='main')
router.register('task_comments_viewset', TaskCommentViewSet, base_name='main')
urlpatterns += router.urls
