from django.template import Library
from tagging.models import Tag
 
register = Library()
 
@register.simple_tag
def snipt_is_favorite(snipt, user):
    return snipt.is_favorite(user)
