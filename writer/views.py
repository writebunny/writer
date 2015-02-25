from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from writer.decorators import credentials_required
from writer.google import GoogleAPI
from writer.google import GoogleCalendar
from writer.google import GoogleDrive


def home(request):
  """Public page for anonymous users."""
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('dashboard'))
  return render_to_response('home.html', {}, RequestContext(request))


@login_required
@credentials_required
def dashboard(request):
  return render_to_response('dashboard.html', {
      'file_list': GoogleDrive().files_list(request.user),
  }, RequestContext(request))


def logout(request):
  auth_logout(request)
  return HttpResponseRedirect(reverse('home'))


def oauth2callback(request):
  if not GoogleAPI().validate_token(request.user, request.REQUEST):
    return HttpResponseRedirect(reverse('error'))
  return HttpResponseRedirect(reverse('home'))


def error(request):
  return render_to_response('error.html', {'user': request.user})

@login_required
@credentials_required
def list_files(request):
  file_id = u'1GB09qxSg11CDJKN_fUr1tM_bNhlAADHw7xnJddvgfM0'
  # GoogleDrive().comments_insert(request.user, file_id=file_id, content='hello world!')
  # GoogleDrive().files_update(request.user, file_id=file_id, description='about this file')

  return render_to_response('files.html', {
      'files': GoogleDrive().files_list(request.user),
      'comments': GoogleDrive().comments_list(request.user, file_id=file_id),
  })


@login_required
@credentials_required
def add_file(request):
  GoogleDrive().files_insert(request.user)
  return HttpResponseRedirect(reverse('list_files'))


@login_required
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
