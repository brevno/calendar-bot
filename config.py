DEBUG = False
HOST = 'localhost'
PORT = 8080
SSL_CONTEXT = ('cert.pem', 'key.pem')

BOT_TOKEN = 'MY_SECRET_TOKEN_HERE'

try:
    from config_local import *
except:
    pass
