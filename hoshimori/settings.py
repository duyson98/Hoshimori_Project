from django.conf import settings as django_settings
from magi.default_settings import DEFAULT_NAVBAR_ORDERING, DEFAULT_ENABLED_PAGES

from hoshimori import models, utils

SITE_NAME = 'Sample Website'
SITE_URL = 'http://sample.com/'
SITE_IMAGE = 'hoshimori.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.sample.com/'
GAME_NAME = 'Sample Game'
DISQUS_SHORTNAME = 'sample'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'

SITE_NAV_LOGO = 'logo.png'

NAVBAR_ORDERING = ['student_list', 'card_list', 'weapon_list', 'material_list'] + DEFAULT_NAVBAR_ORDERING

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['addcard'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['cardcollection'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ON_USER_EDITED = utils.onUserEdited
ON_PREFERENCES_EDITED = utils.onPreferencesEdited