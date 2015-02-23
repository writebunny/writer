from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import session_csrf

session_csrf.monkeypatch()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'writer.views.home', name='home'),
    url(r'^_ah/', include('djangae.urls')),
    # url(r'^login/$', 'writer.views.login', name='login'),
    url(r'^logout/$', 'writer.views.logout', name='logout'),
    url(r'^auth/', include('djangae.contrib.gauth.urls')),
    url(r'^oauth2callback$', 'writer.views.oauth2callback'),
    url(r'^writer/', include('writer.urls')),


    url(r'^error/$', 'writer.views.error', name='error'),



    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
