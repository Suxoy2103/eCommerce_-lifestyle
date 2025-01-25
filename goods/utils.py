from django.db.models import Prefetch
from .models import ProductItem, ProductImage


def get_product_item_queryset(categories=None):
  queryset = ProductItem.objects.select_related("product").prefetch_related(
    "product__category",
    Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="main_image")
  )
  if categories:
    queryset = queryset.filter(product__category__in=categories)
  return queryset