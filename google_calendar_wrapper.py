import shelve
import httplib2
from apiclient.discovery import build
from oauth2client.contrib.dictionary_storage import DictionaryStorage
from oauth2client.client import OAuth2WebServerFlow
import config


class GoogleCalendarWrapper:
    def __init__(self, user_id, redirect_url):
        self.user_id = str(user_id)
        self.flow = OAuth2WebServerFlow(config.GOOGLE_APP_ID,
                                        config.GOOGLE_API_SECRET,
                                        config.GOOGLE_SCOPE,
                                        redirect_url)

    def _get_saved_credentials(self):
        with shelve.open('credentials.dat') as db:
            if self.user_id not in db:
                return None
            storage = DictionaryStorage(db, self.user_id)
            return storage.get()

    @staticmethod
    def _check_authorization(credentials):
        if credentials is None:
            return False
        return not credentials.invalid \
            and (not credentials.access_token_expired)

    def get_events_list(self):
        credentials = self._get_saved_credentials()
        if not self._check_authorization(credentials):
            return {'status': 'error', 'error': 'invalidCredentials'}

        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('calendar', 'v3', http=http)
        request = service.events().list(calendarId='primary')
        try:
            events = request.execute()
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        return events

    def get_authorization_url(self):
        url = self.flow.step1_get_authorize_url(state=self.user_id)
        return url

    def update_credentials(self, auth_code):
        credentials = self.flow.step2_exchange(auth_code)
        with shelve.open('credentials.dat') as db:
            storage = DictionaryStorage(db, self.user_id)
            storage.put(credentials)
