from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

from .validators import validate_product_name, validate_category_name


class BaseModel(models.Model):
  class Meta:
    abstract = True

  def to_json(self, **options):
    from django.core import serializers
    return serializers.serialize('json', [self], indent=2)

  @staticmethod
  def from_json(*serialized_data):
    deserialized_objects = []

    # m2m data does not deserialized. It might be a problem or not
    for item in serialized_data:
      from django.core.serializers import deserialize
      for deserialized in deserialize('json', item):
        deserialized_objects.append(deserialized.object)

    return deserialized_objects


class Image(models.Model):
  file = models.FileField(max_length=1024)
  uploaded_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
  ALL_CATEGORIES = -1

  name = models.CharField(max_length=1024, blank=False, validators=[validate_category_name])
  description = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.name


class Product(BaseModel):
  class Meta:
    indexes = [
      models.Index(fields=['id',])
    ]

  name = models.CharField(max_length=1024, blank=False, validators=[validate_product_name])
  description = models.TextField(null=True, blank=True)
  price = models.DecimalField(max_digits=16, decimal_places=2)
  categories = models.ManyToManyField(Category, related_name='products')
  primary_image = models.ForeignKey(Image,
                                    related_name='primary_image',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
  images = models.ManyToManyField(Image,
                                  related_name='images',
                                  null=True,
                                  blank=True)

  def __str__(self):
    return self.name

  @staticmethod
  def get_from_session(request):
    try:
      serialized_products = request.session['products']
      return Product.from_json(*serialized_products)
    except KeyError:
      return []


class CustomSession(AbstractBaseSession):
  # class Meta(AbstractBaseSession.Meta):
  #   db_table = 'django_session'

  session_data = JSONField(null=True)

  @classmethod
  def get_session_store_class(cls):
    return SessionStore


class SessionStore(DBStore):
  @classmethod
  def get_model_class(cls):
    return CustomSession

  def create_model_instance(self, data):
    obj = super().create_model_instance(data)
    return obj

  def encode(self, session_dict):
    "Return the given session dictionary serialized and encoded as a string."
    return session_dict

  def decode(self, session_data):
    return session_data


@receiver(models.signals.pre_delete, sender=Image)
def remove_file_from_s3(sender, instance: Image, using, **kwargs):
    """This stuff is called before deleting an image"""
    instance.file.delete(save=False)


# @receiver(models.signals.pre_save, sender=Product)
# def generate_slug(sender, instance: Product, using, **kwargs):
#   instance.slug = unique_slug_generator(instance)


def unique_slug_generator(instance, new_slug=None):
  """
  This is for a Django project and it assumes your instance
  has a model with a slug field and a title character (char) field.
  """
  if new_slug is not None:
      slug = new_slug
  else:
    from django.utils.text import slugify
    slug = slugify(instance.name)

  return slug