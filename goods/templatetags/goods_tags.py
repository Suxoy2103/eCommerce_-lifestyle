from django import template

from goods.models import Category

register = template.Library()

@register.simple_tag()
def tag_categories():
    queryset = Category.objects.prefetch_related("parent", "children").order_by("lft")
    return queryset
