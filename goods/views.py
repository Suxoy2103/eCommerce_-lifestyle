from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from .models import Product, ProductItem, Category, ProductImage
from .utils import get_product_item_queryset

class ProductItemListView(ListView):
    model = Product
    template_name = 'goods/shop.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        queryset = get_product_item_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "All products - Shop | Lifestyle"
        context["name"] = "Shop"
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "goods/product_detail.html"
    slug_url_kwarg = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Найти товары того же цвета
        colors = product.colors.all()


        same_products = Product.objects.filter(name=product.name).exclude(id=product.id)

        context['product'] = product
        context["same_products"] = same_products
        context["title"] = f"{product.name} | Lifestyle"
        return context

"""!!! Бьёт ошибка, не могу понять почему."""
class ProductFromCategory(ListView):
    template_name = "goods/shop.html"
    context_object_name = 'products'
    category = None
    paginate_by = 4

    def get_queryset(self):
        slugs = self.kwargs['slug'].split('/')
        category = Category.objects.filter(slug=slugs[0], parent=None).first()  
        for slug in slugs[1:]:
            category = category.children.filter(slug=slug).first()

        self.category = category
        categories = category.get_descendants(include_self=True)
        queryset = get_product_item_queryset(categories)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.category.parent.name}`s {self.category.name} | Lifestyle"
        context["name"] = "Shop"
        return context
