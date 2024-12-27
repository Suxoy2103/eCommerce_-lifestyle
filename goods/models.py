from tkinter import ACTIVE
import uuid
from django.db import models

from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey



class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="Name")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
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

    def get_absolute_url(self):
        return reverse("product_by_category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """add parent slug to slug"""
        if self.parent:
            self.slug = f"{slugify(self.parent.name)}-{slugify(self.name)}"
        # self.slug = unique_slugify(self, self.name, self.slug)

        super().save(*args, **kwargs)


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACT', 'Active'
        INACTIVE = 'INA', 'Inactive'

    name = models.CharField(max_length=150, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    description = models.TextField(blank=True, null=True, verbose_name='Description')

    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount in %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')

    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Categories')

    publish = models.DateTimeField(default=timezone.now, verbose_name='Publish date', blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created date", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated date', blank=True, null=True)

    is_active = models.CharField(max_length=3, choices=Status.choices, default=Status.ACTIVE, verbose_name='Status')

    class Meta:

        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.name} Quantity - {self.quantity}'

    def display_id(self):
        prefix = self.category.get_root()[:1]
        unique_code = str(uuid.uuid4().hex)[:6].upper()
        return f"{prefix}{unique_code}"
    
    def sell_price(self):
        if self.discount:
          return round(self.price - (self.price * self.discount / 100), 2)
        
        return self.price

class ProductImage(models.Model):
    """Model for product images"""
    image = models.ImageField(upload_to='goods_images', verbose_name="Product image")
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='images', verbose_name='Product')
    alt_text = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alt Text')

    def __str__(self):
        return f"Image for {self.product.name}"


# class ShirtSize(models.Model):
#     class Size(models.TextChoices):
#         XS = "XS", "XS"
#         S = "S", "S"
#         M = "M", "M"
#         L = "L", "L"
#         XL = "XL", "XL"
#         XXL = "XXL", "XXL"

#     size = models.CharField(max_length=3, choices=Size.choices, verbose_name="Size")

#     def __str__(self):
#         return self.size


# class PantsSize(models.Model):
#     waist = models.IntegerField()
#     length = models.IntegerField()

#     def __str__(self):
#         return f"{self.waist}/{self.length}"


class ProductSize(models.Model):
    # class SizeType(models.TextChoices):
    #     SHIRTS = 'SHRT', 'Shirts'
    #     PANTS = 'PNT', 'Pants'
    class Shirt_Size(models.TextChoices):
        XS = "XS", "XS"
        S = "S", "S"
        M = "M", "M"
        L = "L", "L"
        XL = "XL", "XL"
        XXL = "XXL", "XXL"

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='sizes', verbose_name='Product')

    # size_type = models.CharField(max_length=4, choices=SizeType.choices, verbose_name='Size type')
    shirt_size = models.CharField(max_length=3, choices=Shirt_Size.choices, null=True, blank=True, verbose_name='Shirt Size')
    # pants_size = models.ForeignKey(PantsSize, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Pants Size')

    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')

    def __str__(self):
        return f"{self.product.name} - {self.shirt_size} - {self.stock}"
