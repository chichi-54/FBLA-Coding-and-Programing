from django.urls import path
from . import views

urlpatterns = [
    path('users', views.all_users, name="all-users"),
    path('applications', views.applications, name="applications"),
]
