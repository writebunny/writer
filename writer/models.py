from apiclient import errors
import logging
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


def get_instance(file_id):
  try:
    return Scene.objects.get(file_id=file_id)
  except Scene.DoesNotExist:
    pass
  try:
    return Chapter.objects.get(file_id=file_id)
  except Chapter.DoesNotExist:
    pass
  try:
    return Book.objects.get(file_id=file_id)
  except Book.DoesNotExist:
    pass


class AbstractFile(models.Model):
  """Abstract class for a model synced with a Google Drive file."""
  TYPE = 'folder'
  MIME_TYPE = 'application/vnd.google-apps.folder'
  file_id = models.CharField(max_length=200, blank=True)
  alternate_link = models.CharField(max_length=200, blank=True)
  pdf_link = models.CharField(max_length=200, blank=True)
  thumbnail_link = models.CharField(max_length=200, blank=True)
  title = models.CharField(max_length=100, blank=True)
  description = models.CharField(max_length=255, blank=True)

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

  def drive_sync(self, from_google=False, data=None):
    """Sync file with Google Drive."""
    service = oauth_service(self.user, 'drive', 'v2')
    if from_google:
      # copy changes from Google drive
      if data is None:
        data = service.files().get(fileId=self.file_id).execute()
      self.title = data.get('title')
      self.description = data.get('description', '')
    else:
      # save changes to Google drive
      body = {
          'title': self.title,
          'description': self.description,
          'mimeType': self.MIME_TYPE,
      }
      if self.parent:
        body['parents'] = [{'id': self.parent.file_id}]
      if self.file_id:
        # update
        data = service.files().update(fileId=self.file_id, body=body).execute()
      else:
        # insert
        data = service.files().insert(body=body).execute()
        self.file_id = data['id']

    self.alternate_link = data['alternateLink']
    if self.MIME_TYPE == 'application/vnd.google-apps.document':
      self.pdf_link = data['exportLinks']['application/pdf']
      self.thumbnail_link = data.get('thumbnailLink', '')
    self.save()

  def deferred_drive_sync(self):
    self.defer_task('drive_sync')


class Book(AbstractFile, models.Model):
  user = models.ForeignKey(User, related_name='books')

  class Meta:
    ordering = ('title',)

  def __unicode__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.title:
      self.title = 'Untitled Book'
    super(Book, self).save(*args, **kwargs)

  @property
  def is_active(self):
    return self.user.extra.book == self

  def touch(self):
    """Set as the user's active book."""
    extra, _ = UserExtra.objects.get_or_create(user=self.user)
    extra.book = self
    extra.save()


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
    if not self.pk:
      self.index = self.book.chapters.count()
    if not self.title:
      self.title = 'Chapter {}'.format(self.index + 1)
    super(Chapter, self).save(*args, **kwargs)


class Scene(AbstractFile, models.Model):
  TYPE = 'document'
  MIME_TYPE = 'application/vnd.google-apps.document'
  user = models.ForeignKey(User, related_name='scenes')
  chapter = models.ForeignKey(Chapter, related_name='scenes')
  index = models.PositiveSmallIntegerField(default=0)
  page_count = models.PositiveIntegerField(default=0)
  word_count = models.PositiveIntegerField(default=0)

  class Meta:
    ordering = ('index',)

  def __unicode__(self):
    return self.title

  @property
  def parent(self):
    return self.chapter

  def save(self, *args, **kwargs):
    if not self.pk:
      self.index = self.chapter.scenes.count()
    if not self.title:
      self.title = 'Scene {}'.format(self.index + 1)
    super(Scene, self).save(*args, **kwargs)


class UserExtra(models.Model):
  """Extra settings for the user."""
  user = models.OneToOneField(User, primary_key=True, related_name='extra')
  book = models.ForeignKey(Book, blank=True, null=True,
                           help_text='Active book.')
  drive_change_id = models.PositiveIntegerField(default=0,
      help_text='Largest change ID from Google drive.')

  def get_list_files(self):
    service = oauth_service(self.user, 'drive', 'v2')
    response = service.files().list(
        q='trashed=false and mimeType="application/vnd.google-apps.document"',
    ).execute()
    return response.get('items')

  def process_drive_changes(self):
    count = 0
    params = {'startChangeId': self.drive_change_id + 1}
    service = oauth_service(self.user, 'drive', 'v2')
    while True:
      try:
        response = service.changes().list(**params).execute()
      except errors.HttpError, error:
        logging.error('HTTP error {}'.format(error))
        return
      items = response.get('items')
      count += len(items)
      for item in items:
        data = item.get('file')
        if data:
          instance = get_instance(file_id=data['id'])
          if instance:
            instance.drive_sync(from_google=True, data=data)

      params['pageToken'] = response.get('nextPageToken')
      if not params['pageToken']:
        break

    if count:
      logging.info('{} changes for {}'.format(count, self.user.email))
    self.drive_change_id = response.get('largestChangeId')
    self.save()
