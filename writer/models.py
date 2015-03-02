from django.contrib.auth import get_user_model
from django.db import models
from google.appengine.ext import deferred

from thirdparty.oauth2 import oauth_service


User = get_user_model()


def run_task(model_name, pk, method_name, **kwargs):
  """Execute a deferred task."""
  model = globals()[model_name]
  instance = model.objects.get(pk=pk)
  method = getattr(instance, method_name)
  method(**kwargs)


class AbstractFile(models.Model):
  """Abstract class for a model synced with a Google Drive file."""

  MIME_TYPE = 'application/vnd.google-apps.folder'
  file_id = models.CharField(max_length=100, blank=True)
  file_link = models.CharField(max_length=100, blank=True)
  title = models.CharField(max_length=100, blank=True)
  description = models.CharField(max_length=255, blank=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta(object):
    abstract = True

  @property
  def parent(self):
    return

  def defer_task(self, method_name):
    deferred.defer(
        run_task,
        model_name=type(self).__name__,
        pk=self.pk,
        method_name=method_name)

  def drive_files_insert(self):
    """Insert file on Google Drive."""
    body={
        'title': self.title,
        'description': self.description,
        'mimeType': self.MIME_TYPE,
    }
    if self.parent:
      body['parents'] = [{'id': self.parent.file_id}]
    service = oauth_service(self.user, 'drive', 'v2')
    response = service.files().insert(body=body).execute()
    self.file_id = response['id']
    self.file_link = response['selfLink']
    self.save()

  def drive_files_update(self):
    """Update a file on Google Drive."""
    service = oauth_service(self.user, 'drive', 'v2')
    response = service.files().update(fileId=self.file_id, body={
        'title': self.title,
        'description': self.description,
    }).execute()


class Book(AbstractFile, models.Model):
  user = models.ForeignKey(User, related_name='books')

  class Meta:
    ordering = ('title',)

  def __unicode__(self):
    return self.title

  def save(self, *args, **kwargs):
    created = self.pk is None
    if not self.title:
      self.title = 'Untitled Book'
    super(Book, self).save(*args, **kwargs)
    if created:
      self.defer_task('drive_files_insert')
    else:
      self.defer_task('drive_files_update')


class Chapter(AbstractFile, models.Model):
  user = models.ForeignKey(User, related_name='chapters')
  book = models.ForeignKey(Book, related_name='chapters')
  index = models.PositiveSmallIntegerField(default=0)

  class Meta:
    ordering = ('index',)

  def __unicode__(self):
    return self.title

  @property
  def parent(self):
    return self.book

  def save(self, *args, **kwargs):
    created = self.pk is None
    if created:
      self.index = self.book.chapters.count()
    if not self.title:
      self.title = 'Chapter {}'.format(self.index + 1)
    super(Chapter, self).save(*args, **kwargs)
    if created:
      self.defer_task('drive_files_insert')
    else:
      self.defer_task('drive_files_update')
