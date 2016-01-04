from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import scad.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scad_back.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', scad.views.index, name='index'),
    url(r'^db', scad.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

)
