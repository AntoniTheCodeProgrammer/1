# TODO: ogarniecie importow - ustrukyrzowanie (np. biblioteka isort), wyrzucenie niepotrzebnych ✅
import io
import math
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .models import Campaign

matplotlib.use("Agg")


# TODO: odpowiednie formatowanie kodu wedlug standardow PEP (np. bibliboteka black) ✅
@login_required
def main_view(request):
    # TODO: dostosowanie nazw funkcji do konwencji PEP (czyli tutaj powinien byc np. main_view - snake case dla nazw funkcji i zmiennych)✅
    campaigns = Campaign.objects.all().order_by("date").values()
    best_campaign = Campaign.objects.all().order_by("-replied").first()

    # TODO: w pythonie korzystamy z onelinerow, zamiast petli for tam gdzie sie da✅
    numbers = [campaign['replied'] for campaign in campaigns]
    names = [campaign['name'] for campaign in campaigns]

    # Stwórz wykres słupkowy
    # plt.barh(name, number, color = "#375BDC")
    # TODO: moja propozycja to zeby ten plot nie byl statyczny i zapisywany do pliku, ale interaktywny
    # mozna to osiagnac np. biblioteka plotly - z tego co kojarze da sie ja zintegrowac z django
    bars = plt.barh(np.arange(len(names)), numbers, color="#375BDC")

    for i, bar in enumerate(bars):
        if bar.get_width() * 1.6 > len(names[i]):
            plt.text(
                bar.get_width() - 1,
                bar.get_y() + bar.get_height() / 2,
                names[i],
                ha="right",
                va="center",
                color="white",
                fontsize=10,
            )
        plt.bar_label(bars, padding=3)
        bar.set_label(names[i])

    plt.xlabel("Ilość Odpowiedzi")
    plt.ylabel("Kampanie")
    plt.title("Zasięg Kampanii")
    l = math.ceil(max(numbers) * 1.1)
    plt.xlim(0, l)
    plt.yticks(np.arange(len(names)), np.arange(1, len(names) + 1))
    plt.legend(title="Nazwy", handles=bars[::-1])

    plt.savefig("mails/static/wykres.jpg")

    # TODO: dodatkowe ploty: response rate, open rate itp. (np. bar plot)
    # TODO: skutecznosc kampanii w czasie - line plot
    context = {
        "mycampaign": best_campaign,
    }
    template = loader.get_template("main.html")
    return HttpResponse(template.render(context, request))


@login_required
def mails_view(request):
    campaigns = Campaign.objects.all()
    template = loader.get_template("campaigns.html")
    context = {
        "campaigns": campaigns,
    }
    return HttpResponse(template.render(context, request))


@login_required
def details_view(request, slug):
    mycampaign = Campaign.objects.get(slug=slug)
    template = loader.get_template("details.html")
    context = {
        "mycampaign": mycampaign,
    }
    return HttpResponse(template.render(context, request))


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # TODO: ladniejsze wyswietlanie errora jak cos nie tak z formularzem
        # typu wiadomosc na czerowno co poszlo nie tak, bo tak to sie zlewa✅

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect("/")
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})
