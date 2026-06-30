from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def rating_stars(rating):
  stars = int(rating)
  html = '<span>'
  for i in range(stars):
    html += '& for i in range(5 - stars): html += '#9733;'
  for i in range(5 - stars):
    html += '&#9734;'
  html += '</span>'

  return mark_safe(html)
    