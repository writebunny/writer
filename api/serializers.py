from django.contrib.auth import get_user_model
from rest_framework import serializers

from writer import models


class Scene(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = models.Scene
    fields = ('url', 'id', 'chapter', 'index', 'title', 'description', 'alternate_link', 'thumbnail_link')
    read_only_fields = ('url', 'id', 'index', 'alternate_link', 'thumbnail_link')


class Chapter(serializers.HyperlinkedModelSerializer):
  scenes = Scene(many=True, read_only=True)

  class Meta:
    model = models.Chapter
    fields = ('url', 'id', 'book', 'index', 'title', 'description', 'scenes')
    read_only_fields = ('url', 'id', 'index')


class Book(serializers.HyperlinkedModelSerializer):
  chapters = Chapter(many=True, read_only=True)

  class Meta:
    model = models.Book
    fields = ('url', 'id', 'title', 'description', 'is_active', 'chapters')
    read_only_fields = ('url', 'id')


class File(serializers.Serializer):
  id = serializers.CharField(max_length=100)
  title = serializers.CharField(max_length=100)
  alternate_link = serializers.CharField(max_length=200, source='alternateLink')
  thumbnail_link = serializers.CharField(max_length=200, source='thumbnailLink')


class User(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('url', 'username', 'email', 'is_staff')
    read_only_fields = ('username', 'email', 'is_staff')
