from django.urls import path
from . import views

urlpatterns = [
    path('all-users/', views.all_users, name="all-users"),
    path('applications/', views.applications, name="applications"),
    path('make-admin/<str:pk>/', views.make_admin, name='make-admin'),
    path('approve-business/<str:pk>/', views.approve_business, name="approve-business"),
    path('decline-business/<str:pk>/', views.decline_business, name="decline-business"),
    path('remove-admin/<str:pk>/', views.remove_admin, name='remove-admin'),
]

