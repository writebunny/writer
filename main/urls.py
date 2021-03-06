from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'writer.views.home', name='home'),
    url(r'^_ah/', include('djangae.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^auth/', include('djangae.contrib.gauth.urls')),
    url(r'^oauth2callback$', 'thirdparty.views.auth_return'),
    url(r'^writer/', include('writer.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
