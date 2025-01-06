from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from .models import Product, Category

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

class ProductFromCategory(ListView):
    template_name = "goods/shop.html"
    context_object_name = 'goods'
    category = None

    def get_queryset(self):
        self.category = Category.objects.filter(slug=self.kwargs['slug'])
        queryset = Product.objects.filter(category__slug=self.category.slug)
        # if not queryset:
        #     sub_cat = Category.objects.filter(parent=self.category)
        #     queryset = Product.objects.filter(category__in=sub_cat)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Записи из категории: {self.category.title}"
        return context