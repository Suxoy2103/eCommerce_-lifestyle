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

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Name")
    slug = models.SlugField(max_length=200, blank=True, verbose_name="URL")
    sku_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='SKU')

    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Description')

    colors = models.ManyToManyField(to='Color', related_name='products', blank=True, verbose_name='Colors')

    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount in %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')

    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Categories')

    publish = models.DateTimeField(default=timezone.now, verbose_name='Publish date', blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created date", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated date', blank=True, null=True)


    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 2)

        return self.price

    def get_absolute_url(self):
        category_slugs = self.category.get_slug_chain()
        return reverse("goods:product_detail", args=[category_slugs, self.slug])

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
    image = models.ImageField(upload_to='goods_images', verbose_name="Product image")
    # thumbnail = models.ImageField(
    #     default="default.jpg",
    #     verbose_name="Product image",
    #     blank=True,
    #     upload_to="images/thumbnails/",
    #     validators=[
    #         FileExtensionValidator(
    #             allowed_extensions=("png", "jpg", "webp", "jpeg", "gif")
    #         )
    #     ],
    # )
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='images', verbose_name='Product')
    alt_text = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alt Text')

    def __str__(self):
        return f"Image for {self.product.name}"

    """for colors"""
    is_main = models.BooleanField(default=False, verbose_name='Main image')


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
