from tkinter import ACTIVE
import uuid
from django.core.validators import FileExtensionValidator
from django.db import models

from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="Name")
    slug = models.SlugField(
        max_length=200, blank=True, null=True, verbose_name="URL", db_index=True)
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
        ancestors = []
        category = self
        while category:
            ancestors.append(category.slug)
            category = category.parent
        return "/".join(reversed(ancestors))
        # ancestors = self.get_ancestors(include_self=True) # get_ancestors - returns a queryset of all ancestors of the current node with the current node included
        # return "/".join(ancestors.values_list("slug", flat=True))

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
    color = models.ForeignKey(to='Color', on_delete=models.CASCADE, related_name='pro_item_col')
    sku_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='SKU')
    original_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    sale_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Sale price')


    class Meta:
        db_table = "product_items"
        verbose_name = "Product Item"
        verbose_name_plural = "Product Items"
        ordering = ['id']

    def get_absolute_url(self):
        category_slugs = self.product.category.get_slug_chain()
        return reverse("goods:product_detail", args=[category_slugs, self.product.slug, self.sku_id])
    
    def save(self, *args, **kwargs):
      if not self.sku_id:
          root = self.product.category.get_root()
          prefix = root.name[:1].upper()
          unique_code = str(uuid.uuid4().hex)[:6].upper()
          self.sku_id = f"{prefix}{unique_code}"
      super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Name")
    slug = models.SlugField(max_length=200, blank=True, verbose_name="URL", unique=True)
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Description')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Categories')
    publish_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Publish date", blank=True, null=True)
    

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to=lambda instance, filename: instance.image_folder(filename),
        default='product_images/default.jpg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], 
        verbose_name="Product item image"
        )
    product_item = models.ForeignKey(to='ProductItem', on_delete=models.CASCADE, related_name='images', verbose_name='Product Item', null=True, blank=True)
    is_main = models.BooleanField(default=False, verbose_name='Main image') # for Photo on the shop page

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    """Function for upload_to(change name of image and create folder)"""
    def image_folder(self, filename):
        unique_iq = uuid.uuid4().hex
        filename = f"{self.product_item.product}-{self.product_item.sku_id}-{unique_iq}." + filename.split('.')[-1]
        folder = f"product_images/{self.product_item.product.category}/{self.product_item.product}/{self.product_item.color}"
        return "{0}/{1}".format(folder, filename)

    def __str__(self):
        return f"Image for {self.image}"


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
