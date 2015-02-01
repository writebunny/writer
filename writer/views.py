from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from writer import oauth2


# @login_required
def home(request):
  return render_to_response('home.html', {
      'user': request.user,
  })


def error(request):
  return render_to_response('error.html')


@login_required
def calendar(request):
  url = oauth2.GoogleCalendar().get_authorize_url(request.user)
  return HttpResponseRedirect(url)


@login_required
def add_event(request):
  import datetime
  client = oauth2.GoogleCalendar()
  client.event_insert(
      user=request.user,
      summary='Dr. Demo appointment',
      location='London, Victoria',
      start=datetime.date(2015, 1, 31),
      end=datetime.date(2015, 1, 31),
      description='Test event from WriteBunny')
  return HttpResponseRedirect(reverse('home'))


@login_required
def oauth2callback(request):
  client = oauth2.GoogleCalendar()
  if not client.validate_token(request.user, request.REQUEST):
    return HttpResponseRedirect(reverse('error'))
  return HttpResponseRedirect(reverse('home'))
