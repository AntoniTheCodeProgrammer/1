from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('campaigns/', views.mails, name='mails'),
    path('campaigns/details/<int:id>', views.details, name='details'),
]