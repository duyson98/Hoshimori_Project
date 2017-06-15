from django.conf import settings as django_settings
from hoshimori import models

SITE_NAME = 'Sample Website'
SITE_URL = 'http://sample.com/'
SITE_IMAGE = 'hoshimori.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.sample.com/'
GAME_NAME = 'Sample Game'
DISQUS_SHORTNAME = 'sample'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'
