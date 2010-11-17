from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.contrib import admin
from django.conf import settings
from snipt.views import *
import os

admin.autodiscover()

import useradmin

urlpatterns = patterns('',
    (r'^api/?', include('snipt.api.urls')),
    (r'^admin/?(.*)', admin.site.root),
    (r'^message/toggle?$', message),
    (r'^wrap/toggle?$', wrap),
    (r'^tags/list/?$', tags),
    (r'^public/tags?$', all_public_tags),
    (r'^delete/?$', delete),
    (r'^save/?$', save),
    (r'^search/?$', search),
    (r'^embed/(?P<snipt>[^/]+)$', embed),
    (r'^password/reset', password_reset),
    (r'^account/set-openid/??$', direct_to_template, {'template': 'registration/set_openid.html'}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^favs/', include('snipt.favsnipt.urls')),
)

urlpatterns += patterns('django_authopenid.views',
    url(r'^yadis.xrdf$', 'xrdf', name='yadis_xrdf'),
    url(r'^%s$' % _('login/?'), 'signin', name='user_signin'),
    url(r'^%s$' % _('logout/?'), 'signout', name='user_signout'),
    url(r'^%s%s$' % (_('signin/'), _('complete/?')), 'complete_signin', name='user_complete_signin'),
    url(r'^%s$' % _('register/'), 'register', name='user_register'),
    url(r'^%s$' % _('signup/?'), 'signup', name='user_signup'),
    url(r'^account/?$', 'account_settings', name='user_account_settings'),
    url(r'^%s$' % _('account/request-password/'), 'sendpw', name='user_sendpw'),
    url(r'^%s%s$' % (_('account/change-password/'), _('confirm/')), 'confirmchangepw', name='user_confirmchangepw'),
    url(r'^%s$' % _('account/change-password/'), 'changepw', name='user_changepw'),
    url(r'^%s$' % _('account/change-email/'), 'changeemail', name='user_changeemail'),
    url(r'^%s$' % _('account/change-openid/'), 'changeopenid', name='user_changeopenid'),
    url(r'^%s$' % _('account/delete/'), 'delete', name='user_delete'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'media').replace('\\','/')}),
    )

urlpatterns += patterns('',
    (r'^(?P<user>[^/]+)?/?(?P<slug>tag/[^/]+)?/?(?P<snipt_id>[^/]+)?/?(all)?$', dispatcher),
)
