from django.shortcuts import render
from  django.template import loader
from django.http import HttpResponse


# Create your views here.
def orders_dashboard(request):
    template = loader.get_template('orders_dashboard.html')
    return HttpResponse(template.render({}, request))

def orders_details(request):
    templates = loader.get_template('orders_details.html')
    return HttpResponse(templates.render({}, request))