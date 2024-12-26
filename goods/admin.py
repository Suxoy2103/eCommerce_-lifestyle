from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from goods.models import Product, ProductImage, ProductSize,Category


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

    # """filter for"""
    # def formfields_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'shirt_size':
    #         kwargs["queryset"] = ShirtSize.objects.all()
    #     elif db_field.name == 'pants_size':
    #         kwargs['queryset'] = PantsSize.objects.all()
    #     return super().formfields_for_foreignkey(db_field, request, **kwargs)
    # class Media:
    #     js = ("vendors/js/admin/product_size_filter.js",)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]
    list_display = ["name", "category", "price", "discount", "quantity", "is_active"]
    search_fields = ["name", "category"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'parent', 'order']
    prepopulated_fields = {"slug": ["name"]}
    ordering = ['order']
