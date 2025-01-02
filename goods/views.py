from django.shortcuts import get_object_or_404, render
from dal import autocomplete

from .models import Product

def shop(request):
    goods = Product.objects.all()
    context = {
        "title": "All products - Shop | Lifestyle",
        "goods": goods
        }
    return render(request, 'goods/shop.html', context)


def product_detail(request, product, category_slugs):
    product = get_object_or_404(Product, slug=product)
    context = {'product': product}
    return render(request, 'goods/product_detail.html', context)

