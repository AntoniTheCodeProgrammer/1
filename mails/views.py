from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Campaign
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

import math

import matplotlib.pyplot as plt
import numpy as np
#TODO: ogarniecie importow - ustrukyrzowanie (np. biblioteka isort), wyrzucenie niepotrzebnych
import io
import sys
import matplotlib
matplotlib.use('Agg')


#TODO: odpowiednie formatowanie kodu wedlug standardow PEP (np. bibliboteka black)
@login_required
def mainView(request):
    #TODO: dostosowanie nazw funkcji do konwencji PEP (czyli tutaj powinien byc np. main_view - snake case dla nazw funkcji i zmiennych)
    campaigns = Campaign.objects.all().order_by('date').values()
    bestCampaign = Campaign.objects.all().order_by('-replied').first()

    name = []
    number = []
    #TODO: w pythonie korzystamy z onelinerow, zamiast petli for tam gdzie sie da
    # numbers = [campaign['replied'] for campaign in campaigns]
    # names = [campaign['name'] for campaign in campaigns]
    for campaign in campaigns:
        name.append(campaign['name'])
        number.append(campaign['replied'])

    # Stwórz wykres słupkowy
    # plt.barh(name, number, color = "#375BDC")
    #TODO: moja propozycja to zeby ten plot nie byl statyczny i zapisywany do pliku, ale interaktywny
    # mozna to osiagnac np. biblioteka plotly - z tego co kojarze da sie ja zintegrowac z django
    bars = plt.barh(np.arange(len(name)), number, color="#375BDC")

    for i, bar in enumerate(bars):
        if bar.get_width()*1.6 > len(name[i]):
            plt.text(bar.get_width()-1, bar.get_y() + bar.get_height()/2, name[i], ha='right', va='center', color='white', fontsize=10)
        plt.bar_label(bars, padding=3)
        bar.set_label(name[i])
        
    plt.xlabel('Ilość Odpowiedzi')
    plt.ylabel('Kampanie')
    plt.title('Zasięg Kampanii')
    l = math.ceil(max(number) * 1.1)
    plt.xlim(0, l)
    plt.yticks(np.arange(len(name)), np.arange(1, len(name)+1))  
    plt.legend(title="Nazwy", handles=bars[::-1])  

    plt.savefig("mails/static/wykres.jpg")

    #TODO: dodatkowe ploty: response rate, open rate itp. (np. bar plot)
    #TODO: skutecznosc kampanii w czasie - line plot
    context = { 
        'mycampaign': bestCampaign,
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context, request))

@login_required
def mailsView(request):
    campaigns = Campaign.objects.all()
    template = loader.get_template('campaigns.html')
    context = {
        'campaigns': campaigns, 
    }
    return HttpResponse(template.render(context, request))

@login_required
def detailsView(request, slug):
    mycampaign = Campaign.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'mycampaign': mycampaign,
    }
    return HttpResponse(template.render(context, request))


def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #TODO: ladniejsze wyswietlanie errora jak cos nie tak z formularzem
        # typu wiadomosc na czerowno co poszlo nie tak, bo tak to sie zlewa
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                
                login(request, user)
                return redirect('/')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
