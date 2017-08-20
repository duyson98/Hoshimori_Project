import time

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from hoshimori import models
from hoshimori.model_choices import *


def generate_settings():
    print 'Get the characters'
    all_students = models.Student.objects.all().order_by('id')
    favorite_characters = [(
        student.pk,
        student.name,
        student.image_url,
    ) for student in all_students]

    print 'Get max stats'
    stats = {
        'hp': None,
        'sp': None,
        'atk': None,
        'def': None,
    }
    evolvables = models.Card.objects.filter(i_rarity__in=EVOLVABLE_RARITIES, i_card_type=0)
    unevolvables = models.Card.objects.exclude(i_rarity__in=EVOLVABLE_RARITIES, i_card_type=0)

    for stat in stats.keys():
        stat_at_70 = stat + "_70"
        # Get max unevolved
        max_evol = getattr(evolvables.order_by("-" + stat_at_70)[0], stat_at_70) + EVOLVED_BONUS_PARAMETER_DICT[stat]
        # Get max evolved
        max_unevol = getattr(unevolvables.order_by("-" + stat_at_70)[0], stat_at_70)

        # Allocate value
        del stats[stat]
        stats[stat + "_max"] = max_evol if max_evol >= max_unevol else max_unevol

    print 'Get latest episode'
    latest_episode = models.Stage.objects.order_by("-episode")[0].episode

    print 'Save generated settings'
    s = u'\
import datetime\n\
FAVORITE_CHARACTERS = ' + unicode(favorite_characters) + u'\n\
MAX_STATS = ' + unicode(stats) + u'\n\
GENERATED_DATE = datetime.datetime.fromtimestamp(' + unicode(time.time()) + u')\n\
LATEST_EPISODE = ' + unicode(latest_episode) + u'\n\
'

    print s
    with open(django_settings.BASE_DIR + '/' + django_settings.SITE + '_project/generated_settings.py', 'w') as f:
        print >> f, s
    f.close()


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
