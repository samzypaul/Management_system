from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader


def home_page(request):
    template = loader.get_template("home.html")
    context = {}
    return HttpResponse(template.render({},request))# render(request,"templates/home.html")#

def about_page(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({},request))