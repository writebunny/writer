from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
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
      serializer.save(user=request.user)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    instance = models.Book.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        instance, data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
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
      serializer.save(user=request.user)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    instance = models.Chapter.objects.get(user=request.user, pk=pk)
    serializer = self.serializer_class(
        instance, data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
