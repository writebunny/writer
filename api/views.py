from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from google.appengine.ext import deferred
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api import serializers
from writer import models
from thirdparty.oauth2 import oauth_required
from thirdparty.oauth2 import oauth_service


def drive_files_insert(user_id, model_name, pk, title, description, mime_type,
                       parent_id=None):
  """Execute a deferred task."""
  User = get_user_model()
  user = User.objects.get(pk=user_id)
  body={
      'title': title,
      'description': description,
      'mimeType': mime_type,
  }
  if parent_id:
    body['parents'] = [{'id': parent_id}]
  service = oauth_service(user, 'drive', 'v2')
  response = service.files().insert(body=body).execute()
  instance = getattr(models, model_name).objects.get(pk=pk)
  instance.file_id = response['id']
  instance.file_link = response['selfLink']
  instance.save()


def drive_files_update(user_id, file_id, title, description):
  """Execute a deferred task."""
  User = get_user_model()
  user = User.objects.get(pk=user_id)
  service = oauth_service(user, 'drive', 'v2')
  response = service.files().update(fileId=file_id, body={
      'title': title,
      'description': description,
  }).execute()


class BookViewSet(viewsets.ModelViewSet):
  queryset = models.Book.objects.all()
  serializer_class = serializers.Book

  def list(self, request):
    serializer = self.serializer_class(
        models.Book.objects.filter(user=request.user),
        context={'request': request},
        many=True)
    return Response(serializer.data)

  def create(self, request):
    serializer = self.serializer_class(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
      instance = serializer.save(user=request.user)
      deferred.defer(
          drive_files_insert,
          user_id=request.user.pk,
          model_name='Book',
          pk=instance.pk,
          title=instance.title,
          description=instance.description,
          mime_type='application/vnd.google-apps.folder')
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    instance = models.Book.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        instance, data=request.data, context={'request': request})
    if serializer.is_valid():
      instance = serializer.save()
      deferred.defer(
          drive_files_update,
          user_id=request.user.pk,
          file_id=instance.file_id,
          title=instance.title,
          description=instance.description)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterViewSet(viewsets.ModelViewSet):
  queryset = models.Chapter.objects.all()
  serializer_class = serializers.Chapter

  def list(self, request):
    book_id = request.QUERY_PARAMS.get('book')
    serializer = self.serializer_class(
        models.Chapter.objects.filter(user=request.user, book_id=book_id),
        context={'request': request},
        many=True)
    return Response(serializer.data)

  def create(self, request):
    serializer = self.serializer_class(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
      instance = serializer.save(user=request.user)
      deferred.defer(
          drive_files_insert,
          user_id=request.user.pk,
          model_name='Chapter',
          pk=instance.pk,
          title=instance.title,
          description=instance.description,
          mime_type='application/vnd.google-apps.folder',
          parent_id=instance.book.file_id)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    instance = models.Chapter.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        instance, data=request.data, context={'request': request})
    if serializer.is_valid():
      instance = serializer.save()
      deferred.defer(
          drive_files_update,
          user_id=request.user.pk,
          file_id=instance.file_id,
          title=instance.title,
          description=instance.description)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
