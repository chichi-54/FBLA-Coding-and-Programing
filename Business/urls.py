from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="businesses"),
    path('business/<str:pk>/', views.single_business, name="single-business"),
    path('create_business', views.create_business, name="create-business"),
    path('update_business/<str:pk>/', views.update_business, name="update-business"),
    path('delete_business/<str:pk>/', views.delete_business, name="delete-business"),
    path('notifications', views.notifications, name="notifications"),
]
