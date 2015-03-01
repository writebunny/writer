"""OAuth2 wrapper for WriteBunny."""
import httplib2
import logging

from django.conf import settings
from googleapiclient import discovery
from oauth2client import xsrfutil
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from writer import models


def inject_service(*service_args):
  """Decorator to inject authenticated service into the API call."""
  def wrap(func):
    def wrapped_func(*args, **kwargs):
      user = args[1]
      service = get_service(user, *service_args)
      if service:
        args += (service,)
        try:
          return func(*args, **kwargs)
        except AccessTokenRefreshError:
          pass
    return wrapped_func
  return wrap


def get_service(user, *path_args):
  """Return authenicated API service."""
  storage = Storage(models.Credential, 'user', user, 'credentials')
  credentials = storage.get()
  if not credentials or credentials.invalid:
    if not credentials:
      logging.warning('No credentials for {}.'.format(user))
    elif credentials.access_token_expired:
      logging.info('Token expired on {}.'.format(credentials.token_expiry))
    else:
      logging.warning('Invalid credentials for {}.'.format(user))
    return
  http = httplib2.Http()
  http = credentials.authorize(http)
  return discovery.build(*path_args, http=http)


class ApiWrapper(object):
  SCOPES = None

  def get_authorize_url(self, user):
    flow = flow_from_clientsecrets(
        settings.OAUTH2_CLIENT_SECRET_FILE,
        redirect_uri=settings.OAUTH2_REDIRECT_URI,
        scope=self.SCOPES)
    flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, user)
    # store per-user flow objects before the first redirection
    storage = Storage(models.Flow, 'user', user, 'flow')
    storage.put(flow)

    return flow.step1_get_authorize_url()

  def validate_token(self, user, data):
    """Handle callback from authentication service and store token."""
    logging.info('Validating token for {}'.format(user.email))
    if user.is_anonymous():
      logging.warning('Can not authenicate anonymous user.')
      return
    state = str(data['state'])  # doesn't like unicode
    if xsrfutil.validate_token(settings.SECRET_KEY, state, user):
      # retrieve flow from storage
      storage = Storage(models.Flow, 'user', user, 'flow')
      flow = storage.get()
      # get and save credentials
      try:
        credentials = flow.step2_exchange(data)
      except FlowExchangeError as error:
        # e.g. access_denied
        logging.warning('Flow exchange error: {}'.format(error))
        return
      storage = Storage(models.Credential, 'user', user, 'credentials')
      storage.put(credentials)
      return True
    else:
      logging.warning('Invalid token: {}'.format(state))
