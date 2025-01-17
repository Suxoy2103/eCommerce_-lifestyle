from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from goods.models import Color, Product, ProductImage, ProductSize, Category, ProductImage


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]
    list_display = ["name", "category", "price", "discount", "quantity"]
    search_fields = ["name", "category"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'parent', 'order']
    prepopulated_fields = {"slug": ["name"]}
    ordering = ['order']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code']
    search_fields = ["name"]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "is_main"]
    list_filter = ["is_main"]
