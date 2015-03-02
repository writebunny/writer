from django.contrib.auth import get_user_model
from django.db import models

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

User = get_user_model()


class Flow(models.Model):
  """OAuth2 flow model."""
  user = models.ForeignKey(User, primary_key=True, related_name='flow')
  flow = FlowField()


class Credentials(models.Model):
  """OAuth2 Credential model."""
  user = models.ForeignKey(User, primary_key=True, related_name='credential')
  credential = CredentialsField()
