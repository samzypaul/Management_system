from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def products_dashboard(request):
    template = loader.get_template('products_dashboard.html')
    return HttpResponse(template.render({}, request))