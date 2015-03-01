from writer.oauth2 import inject_service
from writer.oauth2 import ApiWrapper


class GoogleAPI(ApiWrapper):
  SCOPES = (
      'https://www.googleapis.com/auth/calendar',  # read/write access
      'https://www.googleapis.com/auth/drive.file',  # per-file access
  )


class GoogleCalendar(GoogleAPI):
  """Wrapper for Google Calendar API."""

  @inject_service('calendar', 'v3')
  def events_insert(self, user, service,
                    summary, location, start, end, description):
    return service.events().insert(calendarId='primary', body={
        'summary': summary,
        'location': location,
        'start': {'date': start.isoformat()},
        'end': {'date': end.isoformat()},
        'description': description,
    }).execute()


class GoogleDrive(GoogleAPI):
  """Wrapper for Google Calendar API."""

  @inject_service('drive', 'v2')
  def files_insert(self, user, service, **kwargs):
    # 'application/vnd.google-apps.document'
    return service.files().insert(body=kwargs).execute()

  @inject_service('drive', 'v2')
  def files_update(self, user, service, **kwargs):
    file_id = kwargs.pop('fileId')
    return service.files().update(fileId=file_id, body=kwargs).execute()

  @inject_service('drive', 'v2')
  def files_list(self, user, service):
    return service.files().list().execute()

  @inject_service('drive', 'v2')
  def comments_insert(self, user, service, file_id, content):
    return service.comments().insert(fileId=file_id, body={
        'content': content,
    }).execute()

  @inject_service('drive', 'v2')
  def comments_list(self, user, service, file_id):
    comments = service.comments().list(fileId=file_id).execute()
    return comments.get('items', [])
