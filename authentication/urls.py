from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name = "login"),
    path("register/", views.Register.as_view(), name = "register"),
    path("logout/", views.LogOut.as_view(), name = "logOut")
]