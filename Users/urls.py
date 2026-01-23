from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="businesses"),
    path("login/", views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('account', views.account, name="account"),
    path('create_business', views.create_business, name="create-business"),
    path('update_business', views.update_business, name="update-business"),
    path('delete_business', views.delete_business, name="delete-business"),
    path('inbox', views.inbox, name="inbox"),
]
