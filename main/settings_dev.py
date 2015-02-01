from main.settings import *


DEBUG = True
TEMPLATE_DEBUG = True

CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")

# OAuth2
OAUTH2_CLIENT_SECRET_FILE = os.path.join(
    BASE_DIR, 'main', 'client_secret_dev.json')
OAUTH2_REDIRECT_URI = 'http://dev.writebunny.com:8000/oauth2callback'
