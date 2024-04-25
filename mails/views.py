from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Campaign
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


@login_required
def main(request):
    campaign = Campaign.objects.all().order_by('-replied').values()[0]
    successprocent = []
    # for campaign in campaigns:
    #     successprocent.append((campaign[4]/campaign[6])*100)

    # bestcampaign = successprocent.index(max(successprocent))
    context = {
        'mycampaign': campaign,
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context, request))

@login_required
def mails(request):
    campaigns = Campaign.objects.all()
    template = loader.get_template('campaigns.html')
    context = {
        'campaigns': campaigns, 
    }
    return HttpResponse(template.render(context, request))

@login_required
def details(request, slug):
    mycampaign = Campaign.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'mycampaign': mycampaign,
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})

# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             # log the user in
#             return redirect('main')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
