from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Campaign
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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

def mails(request):
    campaigns = Campaign.objects.all()
    template = loader.get_template('campaigns.html')
    context = {
        'campaigns': campaigns, 
    }
    return HttpResponse(template.render(context, request))

def details(request, slug):
    mycampaign = Campaign.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'mycampaign': mycampaign,
    }
    return HttpResponse(template.render(context, request))


def authView(request):
    if request.thod == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    context = {
        'form' : form,
    }
    template = loader.get_template('signup.html')
    return HttpResponse(template.render(context, request))