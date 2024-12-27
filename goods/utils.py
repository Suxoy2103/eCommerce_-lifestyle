# from uuid import uuid4
# from pytils.translit import slugify


# def unique_slugify(instance, slug, slug_field):
#     """Generate unique slug for model instance"""
#     model = instance.__class__
#     unique_slug = slug_field

#     if not slug:
#         if model.parent:
#             unique_slug = f"{slugify(model.parent.slug)}-{slugify(slug)}"
#         else:
#           unique_slug = slugify(slug)
#     elif (
#         model.objects.filter(slug=slug_field)
#         and model.objects.filter(slug=slug_field).last().id !=
#         instance.id
#     ):
#         unique_slug = f"{slug_field}-{uuid4().hex[:8]}"
#     return unique_slug

