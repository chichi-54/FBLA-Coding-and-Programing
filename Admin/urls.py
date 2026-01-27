from django.urls import path
from . import views

urlpatterns = [
    path('all-users/', views.all_users, name="all-users"),
    path('applications/', views.all_applications, name="applications"),
    path('pending-applications/', views.pending_applications, name="pending-applications"),
    path('approved-applications/', views.approved_applications, name="approved-applications"),
    path('declined-applications/', views.declined_applications, name="declined-applications"),
    path('make-admin/<str:pk>/', views.make_admin, name='make-admin'),
    path('approve-business/<str:pk>/', views.approve_business, name="approve-business"),
    path('decline-business/<str:pk>/', views.decline_business, name="decline-business"),
    path('remove-admin/<str:pk>/', views.remove_admin, name='remove-admin'),
]

