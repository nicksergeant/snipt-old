from django.conf.urls.defaults import *

from snipt.favsnipt.views import *

urlpatterns = patterns('',
    url(r'^toggle/(?P<snipt>.*)$', toggle_fav),
)
