from django.conf.urls import patterns, include, url

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'writer.views.home', name='home'),
    url(r'^oauth2callback$', 'writer.views.oauth2callback'),
    url(r'^calendar/$', 'writer.views.calendar'),
    url(r'^add_event/$', 'writer.views.add_event'),
    url(r'^error/$', 'writer.views.error', name='error'),

    url(r'^_ah/', include('djangae.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
)
