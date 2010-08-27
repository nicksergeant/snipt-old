from tagging.fields import TagField
from tagging.models import Tag
from django.db import models
import tagging

class Ad(models.Model):
    title       = models.TextField()
    url         = models.TextField()
    image       = models.ImageField(upload_to='ads')
    tags        = TagField()
    
    def __unicode__(self):
        return u'%s' %(self.title)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)

tagging.register(Ad, tag_descriptor_attr='_tags') 
