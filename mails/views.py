from django.shortcuts import render
from django.http import HttpResponse

def mails(request):
    return HttpResponse("Mails:")