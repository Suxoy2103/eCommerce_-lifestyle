from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Category


def index(request):
    # categories = Categories.objects.prefetch_related('sub_categories').exclude(name='all products')
    categories = Category.objects.prefetch_related('children').filter(parent__isnull=True).order_by('order')

    context = {
        "title": "lifestyle | Online Fashion, Men`s, Women`s & Kid`s Clothes | lifestyle DE",
        "categories": categories
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": "About us - Lifestyle Group"
    }
    return render(request, 'main/about.html', context)
