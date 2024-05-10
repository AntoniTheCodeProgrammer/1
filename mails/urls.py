from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.main_view, name="main"),
    path("campaigns/", views.mails_view, name="mails"),
    path("campaigns/details/<slug:slug>", views.details_view, name="details"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
