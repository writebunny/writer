from google.appengine.api import users
from django.contrib.auth import get_user

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# @login_required
def home(request):
  return render_to_response('home.html', {
      'user': request.user,
  })
