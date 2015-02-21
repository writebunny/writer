from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from writer.google import GoogleAPI
from writer.models import Credential


def credentials_required(func):
  """Decorator check user has API credentials."""
  def wrapped_func(request, *args, **kwargs):
    try:
      Credential.objects.get(user=request.user)
    except Credential.DoesNotExist:
      url = GoogleAPI().get_authorize_url(request.user)
      return HttpResponseRedirect(url)
    return func(request, *args, **kwargs)
  return wrapped_func
