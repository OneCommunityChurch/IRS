from django.conf.urls import patterns, include, url
from one_info.membership.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_info.views.home', name='home'),
    # url(r'^one_info/', include('one_info.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', index),
)
