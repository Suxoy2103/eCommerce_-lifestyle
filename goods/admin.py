from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from goods.models import Color, Product, ProductImage, Category, ProductItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "category", "sku_id"]
    search_fields = ["product_name", "category", "sku_id"]
    prepopulated_fields = {"product_slug": ["product_name"]}

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'parent', 'order']
    prepopulated_fields = {"slug": ["name"]}
    ordering = ['order']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code']
    search_fields = ["name", "hex_code"]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product_item", "is_main"]
    list_filter = ["is_main"]
