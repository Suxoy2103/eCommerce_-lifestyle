# Generated by Django 4.2.17 on 2025-01-22 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_color_productimage_productitem_productvariation_size_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_slug',
            new_name='slug',
        ),
    ]
