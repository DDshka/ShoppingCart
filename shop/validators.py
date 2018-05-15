from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile


def validate_product_name(value: str):
  from shop.models import Product
  if Product.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"A product \"{value}\" already exists. "
                          f"There can`t be two products with the same name. "
                          f"Do not confuse our customers")


def validate_category_name(value: str):
  from shop.models import Category
  if Category.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"A category \"{value}\" already exists. "
                          f"System does not allow using same names for categories. "
                          f"Enter a unique name")

def validate_image_file(value: str):
  if value:
    ALLOWED_EXTENSIONS = ('png', 'jpeg', 'jpg')
    extension = value[value.rindex('.')+1:]
    if extension not in ALLOWED_EXTENSIONS:
      raise ValidationError("OMAE WA MOU SHINDEIRU")

