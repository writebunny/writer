from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from writer.google import GoogleAPI


def credentials_required(func):
  """Decorator check user has API credentials."""
  def wrapped_func(request, *args, **kwargs):
    if not request.user:
      return HttpResponseRedirect(reverse('home'))
    if not request.user.credential:
      url = GoogleAPI().get_authorize_url(request.user)
      return HttpResponseRedirect(url)
    return func(request, *args, **kwargs)

  return wrapped_func
