from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from writer.decorators import credentials_required
from writer.google import GoogleAPI
from writer.google import GoogleDrive


# @login_required
def home(request):
  return render_to_response('home.html', {
      'user': request.user,
      'files': GoogleDrive().files_list(request.user),
  })


def error(request):
  return render_to_response('error.html')


@login_required
def oauth2callback(request):
  if not GoogleAPI().validate_token(request.user, request.REQUEST):
    return HttpResponseRedirect(reverse('error'))
  return HttpResponseRedirect(reverse('home'))


@credentials_required
def list_files(request):
  return render_to_response('files.html', {
      'files': GoogleDrive().files_list(request.user),
  })


@credentials_required
def add_file(request):
  GoogleDrive().files_insert(request.user)
  return HttpResponseRedirect(reverse('list_files'))
