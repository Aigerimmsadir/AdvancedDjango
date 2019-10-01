from django.urls import path
from . import views

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('logout/', views.logout),
    path('current/', views.current),
    path('register/', views.UserCreate.as_view()),
    path('project_list/', views.ProjectViewSet.as_view()),
    path('project_list/<int:pk>/', views.ProjectDetailAPIView.as_view()),
    path('project_list/<int:pk>/blocks/', views.BlockListAPIView.as_view()),
    path('blocks/<int:pk>/', views.BlockDetailAPIView.as_view()),
    ]