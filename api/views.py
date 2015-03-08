from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api import serializers
from writer import models


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
      book = serializer.save(user=request.user)
      book.drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    book = get_object_or_404(models.Book, user=request.user, pk=pk)
    serializer = self.serializer_class(
        book, data=request.data, context={'request': request})
    if serializer.is_valid():
      book = serializer.save()
      book.deferred_drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @detail_route(methods=['put'])
  def touch(self, request, pk=None):
    book = get_object_or_404(models.Book, user=request.user, pk=pk)
    book.touch()
    return Response()


class ChapterViewSet(viewsets.ModelViewSet):
  queryset = models.Chapter.objects.all()
  serializer_class = serializers.Chapter

  def create(self, request):
    serializer = self.serializer_class(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
      chapter = serializer.save(user=request.user)
      chapter.drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    chapter = get_object_or_404(models.Chapter, user=request.user, pk=pk)
    serializer = self.serializer_class(
        chapter, data=request.data, context={'request': request})
    if serializer.is_valid():
      chapter = serializer.save()
      chapter.deferred_drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SceneViewSet(viewsets.ModelViewSet):
  queryset = models.Scene.objects.all()
  serializer_class = serializers.Scene

  def create(self, request):
    file_id = request.data.get('file_id')
    if file_id and models.Scene.objects.filter(file_id=file_id).count():
      return Response('File already linked.', status=status.HTTP_400_BAD_REQUEST)
    serializer = self.serializer_class(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
      scene = serializer.save(user=request.user)
      if file_id:
        # link to existing Google doc
        scene.file_id = file_id
        scene.drive_sync(from_google=True)
      else:
        scene.drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    scene = get_object_or_404(models.Scene, user=request.user, pk=pk)
    serializer = self.serializer_class(
        scene, data=request.data, context={'request': request})
    if serializer.is_valid():
      scene = serializer.save()
      scene.deferred_drive_sync()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileViewSet(viewsets.ViewSet):
  """
  A simple ViewSet that for listing Google drive files.
  """
  def list(self, request):
    extra, _ = models.UserExtra.objects.get_or_create(user=request.user)
    queryset = extra.get_list_files()
    serializer = serializers.File(queryset, many=True)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
