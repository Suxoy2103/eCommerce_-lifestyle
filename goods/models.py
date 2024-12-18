from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')



    class Meta:
      db_table = 'category'
      verbose_name = 'Category'
      verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    categories = models.ManyToManyField(Categories, verbose_name="Category", related_name="sub_categories")

    class Meta:

        db_table = 'subcategory'
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name




class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount in %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')

    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Category', related_name='products', default='1')
    subcategory = models.ForeignKey(to=SubCategories, on_delete=models.CASCADE, verbose_name='SubCategory', related_name='products')


    class Meta:

        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.name} Quantity - {self.quantity}'
