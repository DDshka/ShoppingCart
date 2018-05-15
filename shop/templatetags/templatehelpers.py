from django import template

register = template.Library()


@register.simple_tag
def relative_url(field_name, value, urlencode=None):
  url = '{}={}'.format(field_name, value)
  if urlencode:
    querystring = urlencode.split('&')
    filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
    encoded_querystring = '&'.join(filtered_querystring)
    url = '?{}&{}'.format(encoded_querystring, url)
  return url


@register.filter('dwr')
def dwr(operand1:int, operand2:int):
  if operand1 is None or operand2 is None:
    return None

  return operand1 % operand2

