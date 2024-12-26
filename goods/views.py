from django.shortcuts import render
from dal import autocomplete

from .models import Product

def shop(request):
    goods = Product.objects.all()
    context = {
        "title": "All products - Shop | Lifestyle",
        "goods": goods
        }
    return render(request, 'goods/shop.html', context)


def product(request):
    return render(request, 'goods/product.html')

