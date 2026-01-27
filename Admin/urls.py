from django.urls import path
from . import views

urlpatterns = [
    path('all-users/', views.all_users, name="all-users"),
    path('applications/', views.applications, name="applications"),
    path('make-admin/<str:pk>/', views.make_admin, name='make-admin'),
    path('remove-admin/<str:pk>/', views.remove_admin, name='remove-admin'),
]

