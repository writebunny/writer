"""OAuth2 wrapper for WriteBunny."""
import httplib2

from django.conf import settings
from googleapiclient import discovery
from oauth2client import xsrfutil
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from writer import models


def inject_service(method):
  """Decorator to inject authenticated service into the API call."""
  def inner(self, **kwargs):
    user = kwargs.pop('user')
    service = self._service(user)
    if service:
      kwargs['service'] = service
      try:
        return method(self, **kwargs)
      except AccessTokenRefreshError:
        pass
  return inner


class ApiWrapper(object):
  SCOPE_URI = None
  SERVICE_ARGS = None

  def _service(self, user):
    """Return authenicated API service."""
    storage = Storage(models.Credential, 'user', user, 'credentials')
    credentials = storage.get()
    if not credentials or credentials.invalid:
      return
    http = httplib2.Http()
    http = credentials.authorize(http)
    return discovery.build(*self.SERVICE_ARGS, http=http)

  def get_authorize_url(self, user):
    flow = flow_from_clientsecrets(
        settings.OAUTH2_CLIENT_SECRET_FILE,
        redirect_uri=settings.OAUTH2_REDIRECT_URI,
        scope=self.SCOPE_URI)
    flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, user)
    # store per-user flow objects before the first redirection
    storage = Storage(models.Flow, 'user', user, 'flow')
    storage.put(flow)

    return flow.step1_get_authorize_url()

  def validate_token(self, user, data):
    """Handle callback from authentication service and store token."""
    state = str(data['state'])  # doesn't like unicode
    if xsrfutil.validate_token(settings.SECRET_KEY, state, user):
      # retrieve flow from storage
      storage = Storage(models.Flow, 'user', user, 'flow')
      flow = storage.get()
      # get and save credentials
      try:
        credentials = flow.step2_exchange(data)
      except FlowExchangeError:
        # e.g. access_denied
        return
      storage = Storage(models.Credential, 'user', user, 'credentials')
      storage.put(credentials)

      return True


class GoogleCalendar(ApiWrapper):
  SCOPE_URI = 'https://www.googleapis.com/auth/calendar'
  SERVICE_ARGS = ('calendar', 'v3')

  @inject_service
  def event_insert(self, service, summary, location, start, end, description):
    return service.events().insert(calendarId='primary', body={
        'summary': summary,
        'location': location,
        'start': {'date': start.isoformat()},
        'end': {'date': end.isoformat()},
        'description': description,
    }).execute()
