from django.contrib.auth import get_user_model
from django.db import models
from oauth2client import django_orm


User = get_user_model()


class Flow(models.Model):
  """OAuth2 flow model."""
  user = models.OneToOneField(User, primary_key=True)
  flow = django_orm.FlowField()


class Credential(models.Model):
  """OAuth2 Credential model."""
  user = models.OneToOneField(User, primary_key=True)
  credentials = django_orm.CredentialsField()
