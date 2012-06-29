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
    url(r'^edit_person/(\d+)/?$', edit_person),
    url(r'^edit_person/', edit_person),
    url(r'^edit_visitor/(\d+)/?$', edit_visitor),
    url(r'^edit_visitor/', edit_visitor),
    url(r'^edit_child/(\d+)/?$', edit_child),
    url(r'^edit_child/', edit_child),
    url(r'^view_person/', view_person),
    url(r'^phone/?$', newPhone),
    url(r'^email/?$', newEmail),
    url(r'^notes/?$', newNote),
    url(r'^parent_guardian/?$', newParentGuardian),
    url(r'^medical_conditions/?$', newMedicalCondition),
    url(r'^view/(partners)/?$', view_people),
    url(r'^view/(visitors)/?$', view_people),
    url(r'^view/(children)/?$', view_people),
    url(r'^tasks/?$', task_list),
    url(r'^edit_task/?$', edit_task),
    url(r'^tasks/(\d+)/?$', edit_task),
    url(r'^view/?$', view_people),
    url(r'^visitor_report/?$', visitorReport),
)
