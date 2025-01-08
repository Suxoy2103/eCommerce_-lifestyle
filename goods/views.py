from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'goods/shop.html'
    context_object_name = 'goods'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "All products - Shop | Lifestyle"
        return context
    


def product_detail(request, product, category_slugs):
    product = get_object_or_404(Product, slug=product)
    context = {'product': product}
    return render(request, 'goods/product_detail.html', context)

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
          category = category.children.filter(slug=slug).first()
          if not category:
              pass
      
      self.category = category
      
      categories = category.get_descendants(include_self=True)

      queryset = Product.objects.filter(category__in=categories)

      return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.category.parent.name}`s {self.category.name} | Lifestyle"
        return context