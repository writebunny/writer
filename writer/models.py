from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class AbstractFile(models.Model):
  file_id = models.CharField(max_length=100, blank=True)
  file_link = models.CharField(max_length=100, blank=True)
  title = models.CharField(max_length=100, blank=True)
  description = models.CharField(max_length=255, blank=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta(object):
    abstract = True


class BookManager(models.Manager):
  def create(self, *args, **kwargs):
    if not kwargs.get('title'):
      kwargs['title'] = 'Untitled Book'
    return super(BookManager, self).create(*args, **kwargs)


class Book(AbstractFile, models.Model):
  objects = BookManager()
  user = models.ForeignKey(User, related_name='books')

  class Meta:
    ordering = ('title',)

  def __unicode__(self):
    return self.title


class ChapterManager(models.Manager):
  def create(self, *args, **kwargs):
    book = kwargs['book']
    kwargs['index'] = book.chapters.count()
    if not kwargs.get('title'):
      kwargs['title'] = 'Chapter {}'.format(kwargs['index'] + 1)
    return super(ChapterManager, self).create(*args, **kwargs)


class Chapter(AbstractFile, models.Model):
  objects = ChapterManager()
  user = models.ForeignKey(User, related_name='chapters')
  book = models.ForeignKey(Book, related_name='chapters')
  index = models.PositiveSmallIntegerField(default=0)

  class Meta:
    ordering = ('index',)

  def __unicode__(self):
    return self.title
