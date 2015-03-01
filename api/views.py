from django.contrib.auth import get_user_model
from google.appengine.ext import deferred
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api import serializers
from writer import models
from writer.google import GoogleDrive


def google_drive(method_name, user_id, **kwargs):
  User = get_user_model()
  user = User.objects.get(pk=user_id)
  method = getattr(GoogleDrive(), method_name)
  method(user, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
  queryset = models.Book.objects.all()
  serializer_class = serializers.Book

  def create(self, request):
    serializer = serializers.Book(
        data=request.data, context={'request': request})
    if serializer.is_valid():
      item = GoogleDrive().files_insert(
          request.user,
          title=serializer.validated_data.get('title'),
          description=serializer.validated_data.get('description'),
          mime_type='application/vnd.google-apps.folder')
      if not item:
        return Response(
            serializer.errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)
      serializer.save(
          user=request.user,
          drive_id=item['id'],
          drive_link=item['selfLink'])
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    book = models.Book.objects.get(pk=pk)
    serializer = serializers.Book(
        book, data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
      deferred.defer(
          google_drive, 'files_update', request.user.pk,
          file_id=book.drive_id,
          title=serializer.validated_data['title'],
          description=serializer.validated_data['description'])
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
