from django.conf.urls.defaults import *

from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from snipt.api.handlers import *
from snipt.api.views import *

auth = HttpBasicAuthentication(realm="Snipt API")
ad = { 'authentication': auth }

tag_handler = Resource(TagHandler)
tags_handler = Resource(TagsHandler)
user_handler = Resource(UserHandler)
snipt_handler = Resource(SniptHandler)

urlpatterns = patterns('',
    (r'^/?$', home),
    url(r'^tags\.(?P<emitter_format>.+)$', tags_handler),
    url(r'^tags/(?P<tag_id>\d+)\.(?P<emitter_format>.+)$', tag_handler),
    url(r'^users/(?P<username>.+)\.(?P<emitter_format>.+)$', user_handler),
    url(r'^snipts/(?P<snipt_id>.+)\.(?P<emitter_format>.+)$', snipt_handler),
)
