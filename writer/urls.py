from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'writer.views.list_files', name='list_files'),
    url(r'^files/add/$', 'writer.views.add_file', name='add_file'),
)
