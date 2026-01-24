from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="businesses"),
    path('business/<str:pk>/', views.single_business, name="single-business"),
    path("login/", views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('account/<str:pk>/', views.account, name="account"),
    path('user_profile', views.account, name="user-profile"),
    path('create_business', views.create_business, name="create-business"),
    path('update_business', views.update_business, name="update-business"),
    path('delete_business', views.delete_business, name="delete-business"),
    path('inbox', views.inbox, name="inbox"),
]
