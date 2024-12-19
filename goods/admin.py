from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from goods.models import Product, Category


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ["name"]}
    ordering = ['order']
