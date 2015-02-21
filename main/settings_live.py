from main.settings import *

SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000 #30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True


SECURE_REDIRECT_EXEMPT = [
    # App Engine doesn't use HTTPS internally, so the /_ah/.* URLs need to be exempt.
    # djangosecure compares these to request.path.lstrip("/"), hence the lack of preceding /
    r"^_ah/"
]

DEBUG = False
TEMPLATE_DEBUG = False

# OAuth2
OAUTH2_CLIENT_ID = '788616750454-3o8tc8d8ebp6r3r10q5faetkdnrqtbg8.apps.googleusercontent.com'
OAUTH2_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'main', 'client_secret_live.json')
OAUTH2_REDIRECT_URI = 'https://writebunny-prod.appspot.com/oauth2callback'
