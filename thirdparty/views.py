import logging
import httplib2

from apiclient.discovery import build
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from thirdparty import models


@login_required
def auth_return(request):
  logging.info('Validating token for {}'.format(request.user))
  state = str(request.REQUEST['state'])  # doesn't like unicode
  if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
    return  HttpResponseBadRequest()
  # retrieve flow from storage
  storage = Storage(models.Flow, 'user', request.user, 'flow')
  flow = storage.get()

  credential = flow.step2_exchange(request.REQUEST)
  storage = Storage(models.Credentials, 'user', request.user, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("/")
