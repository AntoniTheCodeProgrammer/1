from django.urls import path, include
from . import views
from .views import authView

urlpatterns = [
    path('', views.main, name='main'),
    path('campaigns/', views.mails, name='mails'),
    path('campaigns/details/<slug:slug>', views.details, name='details'),
    path('signup/', authView, name="authView"),
    path('accounts/', include('django.contrib.auth.urls')),
]