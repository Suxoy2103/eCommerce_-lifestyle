import re
from django.shortcuts import render


def shop(request):
    return render(request, 'goods/shop.html')


def product(request):
    return render(request, 'goods/product.html')