from django.utils.translation import ugettext_lazy as _

ACCOUNT_TABS = [
    ('Cards', _('Cards'), 'album'),
    ('Weapons', _('Weapons'), 'event'),
    ('About', _('About'), 'about'),
    ('Builder', _('Builder'), 'builder'),
]
ACCOUNT_TABS_LIST = [name for (name, _, _) in ACCOUNT_TABS]
