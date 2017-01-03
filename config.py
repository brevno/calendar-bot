DEBUG = False
HOST = 'localhost'
PORT = 8080
SSL_CONTEXT = ('cert.pem', 'key.pem')

try:
    from config_local import *
except:
    pass
