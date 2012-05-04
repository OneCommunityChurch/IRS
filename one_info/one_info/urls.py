from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login, logout
from one_info.settings import *
from one_info.main.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_info.views.home', name='home'),
    # url(r'^one_info/', include('one_info.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', include('one_info.main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^membership/', include('one_info.membership.urls')),
    url(r'^logout/', logout),
)

urlpatterns+=patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    )


