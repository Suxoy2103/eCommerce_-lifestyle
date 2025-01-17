from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        "title": "lifestyle | Online Fashion, Men`s, Women`s & Children`s Clothes | Lifestyle Group DE"
    }



class AboutView(TemplateView):
    template_name = 'main/about.html'
    extra_context = {"title": "About us - Lifestyle Group", "name": "Contact"}


class ContactView(TemplateView):
    template_name = 'main/contact.html'
    extra_context = {"title": "Contact us - Lifestyle Group", "name": "Contact"}


class FaqView(TemplateView):
    template_name = 'main/faq.html'
    extra_context = {"title": "FAQ`s - Lifestyle Group", "name": "FAQs"}
