from django.contrib.auth import get_user_model
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
      book.sync_insert()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    book = models.Book.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        book, data=request.data, context={'request': request})
    if serializer.is_valid():
      book = serializer.save()
      book.sync_update()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @detail_route(methods=['put'])
  def touch(self, request, pk=None):
    book = models.Book.objects.get(user=request.user, pk=pk)
    extra, _ = models.UserExtra.objects.get_or_create(user=request.user)
    extra.book = book
    extra.save()
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
      chapter.sync_insert()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    chapter = models.Chapter.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        chapter, data=request.data, context={'request': request})
    if serializer.is_valid():
      chapter = serializer.save()
      chapter.sync_update()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SceneViewSet(viewsets.ModelViewSet):
  queryset = models.Scene.objects.all()
  serializer_class = serializers.Scene

  def create(self, request):
    serializer = self.serializer_class(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
      scene = serializer.save(user=request.user)
      scene.drive_files_insert()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    scene = models.Scene.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        scene, data=request.data, context={'request': request})
    if serializer.is_valid():
      scene = serializer.save()
      scene.sync_update()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
