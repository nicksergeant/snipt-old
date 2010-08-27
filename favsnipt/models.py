from django.contrib.auth.models import User
from django.db import models

from snippet.models import Snippet

class FavSnipt(models.Model):
    snipt    = models.ForeignKey(Snippet)
    user     = models.ForeignKey(User)
    created  = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.snipt.description
