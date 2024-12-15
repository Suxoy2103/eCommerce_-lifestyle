from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        "title": "lifestyle | Online Fashion, Men`s, Women`s & Kid`s Clothes | lifestyle DE"
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": "About us - Lifestyle Group"
    }
    return render(request, 'main/about.html', context)
