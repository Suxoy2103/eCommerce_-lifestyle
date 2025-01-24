from django.urls import path
from .views import ProductFromCategory, ProductItemListView, ProductDetailView

from goods import views

app_name = "goods"

urlpatterns = [
    path("", ProductItemListView.as_view(), name="index"),
    path("<path:slug>/", ProductFromCategory.as_view(), name="product_by_category"),
    path(
        "<path:category_slugs>/<slug:product>/<slug:sku_id>", ProductDetailView.as_view(), name="product_detail"
    ),
]
