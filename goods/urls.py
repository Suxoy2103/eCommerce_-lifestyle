from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("", views.shop, name="index"),
    # path("category/<slug:slug>/", views.shop, name="product_by_category"),
    path("<path:category_slugs>/<slug:product>", views.product_detail, name="product_detail"),
]
