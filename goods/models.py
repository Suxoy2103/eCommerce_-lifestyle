from tkinter import ACTIVE
import uuid
from django.core.validators import FileExtensionValidator
from django.db import models

from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="Name")
    slug = models.SlugField(
        max_length=200, blank=True, null=True, verbose_name="URL",)
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Description category")

    order = models.PositiveIntegerField(default=1, verbose_name='Order')

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name="children",
        verbose_name="Parent category",
    )

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order']

        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_slug_for_category", condition=models.Q(parent__isnull=True))
        ]

        constraints.append(
            models.UniqueConstraint(
                fields=["slug", "parent"], name="unique_slug_for_subcategory"
            )
        )

    def get_slug_chain(self):
        slugs = []
        current_node = self
        while current_node:
            slugs.append(current_node.slug)
            current_node = current_node.parent
        return "/".join(reversed(slugs))

    def get_absolute_url(self):
        slug_chain = self.get_slug_chain()
        return reverse("goods:product_by_category", kwargs={'slug': slug_chain})

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Color name")
    hex_code = models.CharField(max_length=7, unique=True, verbose_name="Hex code", help_text="Example: #FFFFFF")

    class Meta:
      db_table = "color"
      verbose_name = "Color"
      verbose_name_plural = "Colors"

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='product_items')
    color = models.ForeignKey(to='Color', on_delete=models.CASCADE, related_name='product_items')
    sku_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='SKU')
    original_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    sale_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Sale price')


    class Meta:
        db_table = "product_items"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
      if not self.sku_id:
          root = self.category.get_root()
          prefix = root.name[:1].upper()
          unique_code = str(uuid.uuid4().hex)[:6].upper()
          self.sku_id = f"{prefix}{unique_code}"
      super(Product, self).save(*args, **kwargs)


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Name")
    product_slug = models.SlugField(max_length=200, blank=True, verbose_name="URL")
    sku_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='SKU')

    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Description')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Categories')


    publish_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Publish date", blank=True, null=True)

    def get_absolute_url(self):
        category_slugs = self.category.get_slug_chain()
        return reverse("goods:product_detail", args=[category_slugs, self.product_slug])

    class Meta:

        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.name} Quantity - {self.quantity}'

    def save(self, *args, **kwargs):
        if not self.sku_id:
            root = self.category.get_root()
            prefix = root.name[:1].upper()
            unique_code = str(uuid.uuid4().hex)[:6].upper()
            self.sku_id = f"{prefix}{unique_code}"
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    """Model for product images"""
    image = models.ImageField(upload_to='goods_images', verbose_name="Product item image")

    product_item = models.ForeignKey(to='ProductItem', on_delete=models.CASCADE, related_name='images', verbose_name='Product Item', null=True, blank=True)
    """for colors"""
    is_main = models.BooleanField(default=False, verbose_name='Main image')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariation(models.Model):
    product_item = models.ForeignKey(to='ProductItem', on_delete=models.CASCADE, related_name='variations', verbose_name='Product Item')
    
    size = models.ForeignKey(to='Size', on_delete=models.CASCADE, related_name='variations', verbose_name='Size')

    qty_in_stock = models.PositiveIntegerField(default=0, verbose_name='Quantity in stock')

    class Meta:
        db_table = 'product_variation'



class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=50, unique=True, verbose_name='Size name')
    sort_order = models.PositiveIntegerField(default=1, verbose_name='Sort order')

    class Meta:
      db_table = 'size_option'
