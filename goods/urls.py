from django.urls import path
from .views import ProductFromCategory, ProductListView

from goods import views

app_name = "goods"

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path(
        "<path:slug>/", ProductFromCategory.as_view(), name="product_by_category"
    ),
    path("<path:category_slugs>/<slug:product>",views.product_detail, name="product_detail"),
]
