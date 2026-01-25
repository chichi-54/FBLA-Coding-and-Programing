from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account, name="account"),
    path('edit_account', views.edit_account, name="edit-account"),
    path('user_profile/<str:pk>/', views.user_profile, name="user-profile"),

]
