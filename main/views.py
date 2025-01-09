from django.http import HttpResponse
from django.shortcuts import render




def index(request):
    context = {
        "title": "lifestyle | Online Fashion, Men`s, Women`s & Kid`s Clothes | lifestyle DE",
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": "About us - Lifestyle Group",
        "name": 'About'
    }
    return render(request, 'main/about.html', context)


def contact(request):
    context = {
        "title": "Contact us - Lifestyle Group",
        "name": 'Contact'
               }

    return render(request, "main/contact.html", context)


def faq(request):
    context = {
        "title": "FAQ`s - Lifestyle Group",
        "name": 'FAQs'
        }
    return render(request, "main/faq.html", context)
