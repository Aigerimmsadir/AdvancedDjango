from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('current/', views.current),
    path('register/', views.UserCreate.as_view()),
    path('categories/', views.category_list),
    path('categories/<int:pk>/', views.category_detail),
    path('categories/<int:pk>/advertisements/', views.AdvertisementList.as_view()),
    path('advertisements/<int:pk>/', views.AdvertisementDetail.as_view()),
    path('advertisements/<int:pk>/comments/', views.Comments.as_view()),

]