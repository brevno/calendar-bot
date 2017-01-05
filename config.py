DEBUG = False
HOST = 'localhost'
PORT = 8080
SSL_CONTEXT = ('cert.pem', 'key.pem')

BOT_TOKEN = 'MY_SECRET_TOKEN_HERE'

GOOGLE_APP_ID = '202020-2222222.apps.googleusercontent.com'
GOOGLE_API_SECRET = 'VERY_SECRET'
GOOGLE_SCOPE = 'https://www.googleapis.com/auth/calendar'


try:
    from config_local import *
except:
    pass
