from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from thirdparty.oauth2 import oauth_required
from writer import models


def home(request):
  """Public page for anonymous users."""
  return render_to_response('writer/home.html', {}, RequestContext(request))


@login_required
@oauth_required(settings.GOOGLE_SCOPE)
def dashboard(request):
  extra, _ = models.UserExtra.objects.get_or_create(user=request.user)
  extra.process_drive_changes()
  return render_to_response('writer/dashboard.html', {}, RequestContext(request))
