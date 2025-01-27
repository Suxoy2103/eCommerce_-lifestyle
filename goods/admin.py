from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from goods.models import Color, Product, ProductImage, Category, ProductItem
import nested_admin



class ProductImageInline(nested_admin.NestedStackedInline):
    model = ProductImage
    extra = 1

class ProductItemInline(nested_admin.NestedStackedInline):
    model = ProductItem
    inlines = [ProductImageInline]
    extra = 1
    fields = ("color", "original_price", "sale_price")
    

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        "name",
        "category",
      )
    search_fields = ["name", "category"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [ProductItemInline]

@admin.register(ProductItem)
class ProductItemAdmin(nested_admin.NestedModelAdmin):
    list_display = ["product", "color", "sku_id"]
    search_fields = ["product", "color", "sku_id"]
    fields = (
      "product",
      "color",
      "original_price",
      "sale_price",  
    )
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
    list_filter = ["product_item","is_main"]
