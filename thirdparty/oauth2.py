import logging
import httplib2

from apiclient.discovery import build
from django.conf import settings
from django.http import HttpResponseRedirect
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from thirdparty import models

def oauth_required(scope):
  """Completes all OAuth 2.0 steps before entering the function."""
  def wrap(func):
    def wrapped_func(request, *args, **kwargs):
      storage = Storage(models.Credentials, 'user', request.user, 'credential')
      credential = storage.get()
      if not credential or credential.invalid:
        flow = flow_from_clientsecrets(
            settings.OAUTH2_CLIENT_SECRET_FILE,
            redirect_uri=settings.OAUTH2_REDIRECT_URI,
            scope=scope)
        flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        # store per-user flow objects before the first redirection
        storage = Storage(models.Flow, 'user', request.user, 'flow')
        storage.put(flow)

        authorize_url = flow.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
      else:
        return func(request, *args, **kwargs)
    return wrapped_func
  return wrap


def oauth_service(user, *args):
  storage = Storage(models.Credentials, 'user', user, 'credential')
  credential = storage.get()
  if not credential or credential.invalid:
    logging.error('Invalid credentials for {}'.format(user))
  else:
    logging.info('Loading service {}'.format(args))
    http = httplib2.Http()
    http = credential.authorize(http)
    return build(*args, http=http)
