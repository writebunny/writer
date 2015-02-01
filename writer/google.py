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
  def files_insert(self, user, service):
    return service.files().insert(body={
        'title': 'test doc',
        'mimeType': 'application/vnd.google-apps.document',
    }).execute()

  @inject_service('drive', 'v2')
  def files_list(self, user, service):
    return service.files().list().execute()
