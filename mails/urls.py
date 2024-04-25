from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('campaigns/', views.mails, name='mails'),
    path('campaigns/details/<slug:slug>', views.details, name='details'),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]