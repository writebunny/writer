from django.contrib.auth import get_user_model
from rest_framework import serializers

from writer import models


class Chapter(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = models.Chapter
    fields = ('url', 'id', 'book', 'index', 'title', 'description', 'created')
    read_only_fields = ('id', 'index', 'created')


class Book(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = models.Book
    fields = ('url', 'id', 'title', 'description', 'created')
    read_only_fields = ('id', 'created')


class User(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('url', 'username', 'email', 'is_staff')
    read_only_fields = ('username', 'email', 'is_staff')
