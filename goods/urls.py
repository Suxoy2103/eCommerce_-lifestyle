from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("", views.shop, name="index"),
    path("product/", views.product, name="product"),
]
