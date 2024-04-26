from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.mainView, name='main'),
    path('campaigns/', views.mailsView, name='mails'),
    path('campaigns/details/<slug:slug>', views.detailsView, name='details'),
    path('signup/', views.signupView, name="signup"),
    path('login/', views.loginView, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]