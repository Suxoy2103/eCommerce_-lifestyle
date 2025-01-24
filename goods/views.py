from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from .models import Product, ProductItem, Category, ProductImage


class ProductItemListView(ListView):
    model = Product
    template_name = 'goods/shop.html'
    context_object_name = 'goods'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "All products - Shop | Lifestyle"
        context["name"] = "Shop"
        context["products"] = ProductItem.objects.select_related(
            "product"
        ).prefetch_related('product__category',
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_main=True).order_by("id"),
            )

        )
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
    context_object_name = 'goods'
    category = None
    paginate_by = 4

    def get_queryset(self):
        slugs = self.kwargs['slug'].split('/')
        category = Category.objects.filter(slug=slugs[0], parent=None).first()  



        if not category:
            pass

        for slug in slugs[1:]:
            category = category.children.filter(slug=slug).first() # !!! Бьёт ошибка, не могу понять почему.
            if not category:
                pass

        self.category = category

        categories = category.get_descendants(include_self=True)

        queryset = Product.objects.filter(category__in=categories)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.category.parent.name}`s {self.category.name} | Lifestyle"
        context["name"] = "Shop"
        return context
