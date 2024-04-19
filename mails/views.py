from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Campaign


def mails(request):
    campaigns = Campaign.objects.all().values()
    template1 = loader.get_template('first.html')
    template = loader.get_template('campaigns.html')
    context = {
        'campaigns': campaigns, 
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
  mycampaign = Campaign.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mycampaign': mycampaign,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())