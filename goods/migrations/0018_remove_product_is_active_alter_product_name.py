# Generated by Django 4.2.17 on 2025-01-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_color_productimage_is_main_product_colors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
        ),
    ]
