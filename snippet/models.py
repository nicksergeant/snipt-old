from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from django.db import models
import tagging

class Snippet(models.Model):
    code         = models.TextField()
    description  = models.TextField()
    slug         = models.SlugField()
    lexer        = models.TextField()
    key          = models.TextField()
    created      = models.DateTimeField(auto_now_add=True)
    user         = models.ForeignKey(User)
    public       = models.BooleanField()
    tags         = TagField()
    
    def __unicode__(self):
        return u'%s' %(self.description)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self) 
    
    def get_absolute_url(self):
        return "/%s/%s/" % (self.user.username, self.slug)
    
    def is_favorite(self, user):
        from snipt.favsnipt.models import FavSnipt
        try:
            FavSnipt.objects.get(snipt=self, user=user)
            return 'favorited'
        except:
            return ''

try:
    tagging.register(Snippet, tag_descriptor_attr='_tags') 
except tagging.AlreadyRegistered:
    pass

class Referer(models.Model):
    url          = models.URLField()
    snippet      = models.ForeignKey(Snippet)
    
    def __unicode__(self):
        return u'%s' %(self.url)