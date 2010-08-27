from snipt.snippet.models import Snippet
from django.template import Library
from tagging.models import Tag
 
register = Library()
 
@register.simple_tag
def snipt_count(user):
    return Snippet.objects.filter(user=user).count()

@register.simple_tag
def tag_count(user):
    return len(Tag.objects.usage_for_queryset(Snippet.objects.filter(user=user)))
