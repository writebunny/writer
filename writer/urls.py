from django.conf.urls import patterns, url


urlpatterns = patterns('writer.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^files/add/$', 'add_file', name='add_file'),
    url(r'^calendar/add/$', 'add_event', name='add_event'),
)
