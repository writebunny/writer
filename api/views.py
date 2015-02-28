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

  def create(self, request):
    serializer = serializers.Book(
        data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
  model = get_user_model()
  queryset = model.objects.all()
  serializer_class = serializers.User
