from django.db import models

class Product(models.Model):
  name = models.CharField(max_length=150, verbose_name="Name")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

  description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Description")

  tags = ""
  category = ""
  collection = ""
  color = ""
  size = ""
  stack = ""