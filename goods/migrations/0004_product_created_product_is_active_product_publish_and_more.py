# Generated by Django 4.2.17 on 2024-12-20 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_alter_category_options_category_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created date'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.CharField(choices=[('ACT', 'Active'), ('INA', 'Inactive')], default='ACT', max_length=3, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='product',
            name='publish',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Publish date'),
        ),
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='goods_images', verbose_name='Product image'),
        ),
    ]
