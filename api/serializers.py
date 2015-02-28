from django.contrib.auth import get_user_model
from rest_framework import serializers

from writer import models


class Book(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = models.Book
    fields = ('url', 'id', 'title', 'description', 'created')


class User(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('url', 'username', 'email', 'is_staff')
