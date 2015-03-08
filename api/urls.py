from django.conf.urls import url, include
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'files', views.FileViewSet, base_name='files')
router.register(r'scenes', views.SceneViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
