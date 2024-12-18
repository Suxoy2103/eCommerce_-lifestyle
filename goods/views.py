import re
from django.shortcuts import render

from .models import SubCategories
from dal import autocomplete

def shop(request):
    context = {
        "title": "All products - Shop | Lifestyle",
        "goods": [
            {
                "image": "vendors/images/products/fashion-store-product-01.jpg",
                "name": "Textured sweater",
                "price": "$200.00",
            },
            {
                "image": "vendors/images/products/fashion-store-product-02.jpg",
                "name": "Traveller shirt",
                "price": "$350.00",
            },
            {
                "image": "vendors/images/products/fashion-store-product-03.jpg",
                "name": "Crewneck sweatshirt",
                "price": "$220.00",
            },
        ],
    }
    return render(request, 'goods/shop.html', context)


def product(request):
    return render(request, 'goods/product.html')

