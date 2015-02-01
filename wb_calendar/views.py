import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from writer.decorators import credentials_required
from writer.google import GoogleCalendar


@credentials_required
def add_event(request):
  GoogleCalendar().events_insert(
      request.user,
      summary='Dr. Demo appointment',
      location='London, Victoria',
      start=datetime.date(2015, 1, 31),
      end=datetime.date(2015, 1, 31),
      description='Test event from WriteBunny')
  return HttpResponseRedirect(reverse('home'))
