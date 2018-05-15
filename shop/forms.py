from django import forms

from shop.validators import validate_image_file
from .models import *


class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ('name', 'description',)
    widgets = {
      'name': forms.TextInput(attrs={'placeholder': 'Enter category name...'}),
    }


class ProductForm(forms.ModelForm):
  primary_image = forms.CharField(required=False, widget=forms.HiddenInput(), validators=[validate_image_file])
  images = forms.CharField(required=False, widget=forms.HiddenInput(), validators=[validate_image_file])

  class Meta:
    model = Product
    fields = ('name', 'description', 'price', 'categories', 'primary_image', 'images')
    widgets = {
      'name': forms.TextInput(attrs={'placeholder': 'Enter product name...'}),
      'price': forms.TextInput(attrs={'placeholder': 'Enter product price...'}),
      'categories': forms.CheckboxSelectMultiple(),
    }

  def save(self, commit=True) -> Product:
    name = self.cleaned_data.get('name')
    description = self.cleaned_data.get('description')
    categories = self.cleaned_data.get('categories')
    price = str(self.cleaned_data.get('price'))
    primary_image = self.cleaned_data.get('primary_image')
    images = self.cleaned_data.get('images')

    instance: Product = Product.objects.create(name=name,
                                               description=description,
                                               price=price)
    for category in categories:
      instance.categories.add(category)

    if primary_image:
      instance.primary_image = primary_image

    if images:
      for image in images:
        instance.images.add(image)

    instance.save()

    return instance

  def clean_primary_image(self):
    image_url = self.cleaned_data.get('primary_image')
    if not image_url:
      return None
    last_slash_index = image_url.rindex('/') + 1
    filename = image_url[last_slash_index:]
    image = Image.objects.create(file=filename)
    return image

  def clean_images(self):
    image_urls = self.cleaned_data.get('images')
    if not image_urls:
      return None

    from rest_framework.utils import json
    image_urls = json.loads(image_urls)
    images = []
    for url in image_urls:
      last_slash_index = url.rindex('/') + 1
      filename = url[last_slash_index:]
      images.append(Image.objects.create(file=filename).id)

    return images


class ProductImagesForm(forms.Form):
  primary_image_file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}))
  images_files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'}))


class AddToCartForm(forms.Form):
  product = forms.IntegerField(widget=forms.HiddenInput())

  def clean_product(self):
    product_id = self.cleaned_data.get('product')
    return Product.objects.get(id=product_id)


class SearchForm(forms.Form):
  """
  Django form for search.
  Maybe something there can be made more wisely

  -1 is for 'All categories'
  Keep it in mind
  """

  # It could be better somehow
  AVAILABLE_ORDERS = ("name", "-name", "price", "-price")
  DEFAULT_ORDER = "name"

  q = forms.CharField(max_length=1024,
                      label="Search query",
                      widget=forms.TextInput(attrs={'class': 'form-control'}))
  categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
  order = forms.CharField(max_length=1024)
  page = forms.CharField(max_length=9999)

  def __init__(self, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    category_options = Category.objects.all()
    choices = [(x.id, x.name) for x in category_options]
    choices.append((Category.ALL_CATEGORIES, 'All categories',))

    self.fields['q'].required = False
    self.fields['q'].value = ''

    self.fields['page'].widget = forms.HiddenInput()
    self.fields['page'].initial = '1'
    self.fields['page'].required = False

    self.fields['order'].widget = forms.HiddenInput()
    self.fields['order'].initial = self.DEFAULT_ORDER
    self.fields['order'].required = False

    self.fields['categories'].required = False
    self.fields['categories'].choices = choices
    self.fields['categories'].initial = [-1]

  def clean_categories(self):
    categories = self.cleaned_data.get('categories')
    if not categories:
      return [-1]

    categories = [int(x) for x in categories]
    return categories

  def clean_order(self):
    order = self.cleaned_data.get('order')
    if (not order) or (order not in self.AVAILABLE_ORDERS):
      return self.DEFAULT_ORDER

    return order

  def clean_page(self):
    page = self.cleaned_data.get('page')
    if not page:
      return 1

    return int(page)