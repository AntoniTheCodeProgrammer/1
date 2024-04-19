from django.urls import path
from . import views

urlpatterns = [
    path('', views.mails, name='mails'),
    path('details/<int:id>', views.details, name='details'),
]