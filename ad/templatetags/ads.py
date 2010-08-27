from tagging.models import TaggedItem
from snipt.ad.models import Ad
from django import template

register = template.Library()

@register.simple_tag
def ad(tag):
    try:
        ads = TaggedItem.objects.get_by_model(Ad.objects.order_by('?'), tag)
        ad = ads[0]
    except:
        ads = Ad.objects.order_by('?')
        ad = ads[0]
        tag = ''
    return """
        <h1 style="margin-bottom: 20px; padding-top: 15px;">A good %s read</h1>
        <div class="amazon-book clearfix">
            <div class="amazon-title">
                <a href="%s" rel="nofollow" class="clearfix">
                    <img src="/media/%s" alt="%s" title="%s" />
                    %s
                </a>
            </div>
        </div>
        """ % (tag,
               ad.url,
               ad.image,
               ad.title,
               ad.title,
               ad.title)

