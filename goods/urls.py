from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("", views.shop, name="index"),
    # path("category/<slug:slug>/", views.shop, name="product_by_category"),
    path("product/", views.product, name="product"),
]
