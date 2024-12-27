from django import template

from goods.models import Category

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Category.objects.prefetch_related("children").all().order_by("lft")
