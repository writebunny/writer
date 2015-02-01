from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^event/add/$', 'wb_calendar.views.add_event', name='add_event'),
)
