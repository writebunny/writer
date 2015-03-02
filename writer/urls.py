from django.conf.urls import patterns, url


urlpatterns = patterns('writer.views',
    url(r'^$', 'dashboard', name='dashboard'),
)
