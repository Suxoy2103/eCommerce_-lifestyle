from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.forms import ValidationError

from .models import ProductImage

@receiver(post_save, sender=ProductImage)
def check_single_main_image(sender, instance, created, **kwargs):
    if instance.is_main:
        ProductImage.objects.filter(
            product_item=instance.product_item,
            is_main=True
        ).exclude(pk=instance.pk).update(is_main=False)

