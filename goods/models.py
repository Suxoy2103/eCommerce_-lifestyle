from django.db import models

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

    def save(self, *args, **kwargs):
        """add parent slug to slug"""
        if self.parent:
            self.slug = f'{slugify(self.parent.slug)}-{self.slug}'
        
        super().save(*args, **kwargs)
    

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount in %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')

    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Categories')


    class Meta:

        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.name} Quantity - {self.quantity}'
