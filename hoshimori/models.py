# -*- coding: utf-8 -*-
from __future__ import division

import os

from django.conf import settings as django_settings
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _, string_concat
from web.item_model import ItemModel, get_image_url, get_http_image_url
from web.models import User
from web.utils import tourldash, randomString

from hoshimori.django_translated import t
from hoshimori.model_choices import *


############################################################
# Utils

@deconstructible
class uploadItem(object):
    def __init__(self, prefix, length=30):
        self.prefix = prefix
        self.length = length

    def __call__(self, instance, filename):
        _, extension = os.path.splitext(filename)
        if not extension:
            extension = '.png'
        return u'{static_uploaded_files_prefix}{prefix}/{id}{string}{extension}'.format(
            static_uploaded_files_prefix=django_settings.STATIC_UPLOADED_FILES_PREFIX,
            prefix=self.prefix,
            id=instance.id if instance.id else randomString(6),
            string=tourldash(unicode(instance)),
            extension=extension,
        )


def getAccountLeaderboard(account):
    if not account.level:
        return None
    return Account.objects.filter(level__gt=account.level).values('level').distinct().count() + 1


############################################################
# Student

class Student(ItemModel):
    collection_name = 'student'

    name = models.CharField(string_concat(_('Name'), ' (romaji)'), max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    description = models.CharField(_('Description'), max_length=100)

    i_school_year = models.PositiveIntegerField(_('School year'), choices=SCHOOL_YEAR_CHOICES, null=True)

    @property
    def school_year(self):
        if self.i_school_year is not None:
            return SCHOOL_YEAR_DICT[self.i_school_year]
        else:
            return None

    birthday = models.DateField(_('Birthday'), null=True)

    i_star_sign = models.PositiveIntegerField(_('Star sign'), choices=STAR_SIGN_CHOICES,
                                              null=True)

    @property
    def star_sign(self):
        if self.i_star_sign is not None:
            return STAR_SIGN_DICT[self.i_star_sign]
        else:
            return None

    @property
    def english_star_sign(self):
        if self.i_star_sign is not None:
            return ENGLISH_STAR_SIGN_DICT[self.i_star_sign]
        else:
            return None

    i_blood_type = models.PositiveIntegerField(_('Blood type'), choices=BLOOD_TYPE_CHOICES, null=True)

    @property
    def blood_type(self):
        if self.i_blood_type is not None:
            return BLOOD_TYPE_DICT[self.i_blood_type]
        else:
            return None

    extra_activity = models.CharField(_('Extracurricular activity'), max_length=100)
    catchphrase_1 = models.CharField(_('Catchphrase 1'), max_length=100)
    catchphrase_2 = models.CharField(_('Catchphrase 2'), max_length=100)
    height = models.PositiveIntegerField(_('Height'), null=True, help_text='in cm')
    weight = models.PositiveIntegerField(_('Weight'), null=True, help_text='in kg')
    bust = models.PositiveIntegerField(_('Bust'), null=True, help_text='in cm')
    waist = models.PositiveIntegerField(_('Waist'), null=True, help_text='in cm')
    hip = models.PositiveIntegerField(_('Hip'), null=True, help_text='in cm')
    hobby_1 = models.CharField(_('Hobby 1'), max_length=100)
    hobby_2 = models.CharField(_('Hobby 2'), max_length=100)
    hobby_3 = models.CharField(_('Hobby 3'), max_length=100)
    food_likes = models.CharField(_('Liked food'), max_length=100)
    food_dislikes = models.CharField(_('Disliked food'), max_length=100)
    family = models.CharField(_('Family members'), max_length=100)
    dream = models.CharField(_('Dream job'), max_length=100)
    ideal_1 = models.CharField(_('Ideal person 1'), max_length=100)
    ideal_2 = models.CharField(_('Ideal person 2'), max_length=100)
    ideal_3 = models.CharField(_('Ideal person 3'), max_length=100)
    pastime = models.CharField(_('Pastime'), max_length=100)
    destress = models.CharField(_('Destress'), max_length=100)
    fav_memory = models.CharField(_('Favorite memory'), max_length=100)
    fav_phrase = models.CharField(_('Favorite phrase'), max_length=100)
    secret = models.CharField(_('Secret'), max_length=5000)

    CV = models.CharField(_('CV'), help_text='In Japanese characters.', max_length=100)
    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100)

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))


############################################################
# Account

class Account(ItemModel):
    collection_name = 'account'

    owner = models.ForeignKey(User, related_name='accounts')
    creation = models.DateTimeField(_('Join Date'), auto_now_add=True)
    start_date = models.DateField(null=True, verbose_name=_('Start Date'),
                                  help_text=_('When you started playing with this account.'))
    level = models.PositiveIntegerField(_('Level'), null=True, db_index=True)
    nickname = models.CharField(_('Nickname'), max_length=100)
    game_id = models.CharField(_('Game ID'), max_length=8)
    device = models.CharField(_('Device'), max_length=150)
    i_os = models.PositiveIntegerField(_('Operating System'), choices=OS_CHOICES, default=0)

    @property
    def has_os(self):
        return self.i_os is not None

    @property
    def os(self):
        if self.i_os is not None:
            return OS_DICT[self.i_os]
        else:
            return None

    i_player_type = models.PositiveIntegerField(_('Player type'), choices=PLAYERTYPE_CHOICES, default=0)

    @property
    def player_type(self):
        if self.i_player_type is not None:
            return PLAYERTYPE_DICT[self.i_player_type]
        else:
            return None

    @property
    def item_url(self):
        return self.owner.item_url

    @property
    def full_item_url(self):
        return self.owner.full_item_url

    @property
    def http_item_url(self):
        return self.owner.http_item_url

    def __unicode__(self):
        return u'#{} Level {}'.format(self.id, self.level)


############################################################
# Card

class Card(ItemModel):
    collection_name = 'card'

    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)
    owner = models.ForeignKey(User, related_name='added_cards')
    student = models.ForeignKey(Student, verbose_name=_('Student'), related_name='cards', null=True,
                                on_delete=models.SET_NULL)

    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=RARITY_CHOICES)

    @property
    def rarity(self):
        return RARITY_DICT[self.i_rarity]

    i_weapon = models.PositiveIntegerField(_('Weapon'), choices=WEAPON_CHOICES)

    @property
    def weapon(self):
        return WEAPON_DICT[self.i_weapon]

    @property
    def english_weapon(self):
        return ENGLISH_WEAPON_DICT[self.i_weapon]

    name = models.CharField(_('Title'), max_length=100)

    def __unicode__(self):
        return self.name

    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100)

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('c'))

    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'))

    @property
    def art_url(self):
        return get_image_url(self.art)

    @property
    def http_art_url(self):
        return get_http_image_url(self.art)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'))

    @property
    def transparent_url(self):
        return get_image_url(self.transparent)

    @property
    def http_transparent_url(self):
        return get_http_image_url(self.transparent)

    # Sub card effect
    subcard_effect = models.BooleanField(_('Subcard Effect'), default=False)

    # Card type
    card_type = models.PositiveIntegerField(_('Card Type'), choices=CARDTYPE_CHOICES)

    @property
    def is_subcard(self):
        return self.card_type == 2

    @property
    def is_evolved(self):
        return (False, True)

    # Parameter
    hp_1 = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Level 1'), ')'), default=0)
    hp_50 = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Level 50'), ')'), default=0)
    hp_70 = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Level 70'), ')'), default=0)
    sp_1 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 1'), ')'), default=0)
    sp_50 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 50'), ')'), default=0)
    sp_70 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 70'), ')'), default=0)
    atk_1 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 1'), ')'), default=0)
    atk_50 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 50'), ')'), default=0)
    atk_70 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 70'), ')'), default=0)
    def_1 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 1'), ')'), default=0)
    def_50 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 50'), ')'), default=0)
    def_70 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 70'), ')'), default=0)

    def _exp_at_level(self, level=1):
        return int(EXP_TO_NEXT_LEVEL[level - 1] * (1 + self.i_rarity) / 5)

    def _total_exp_needed(self, level):
        return int(ACCUMULATIVE_EXP[level - 1] * (1 + self.i_rarity) / 5)

    @property
    def overall_max(self):
        return self.hp_70 + self.sp_70 + self.atk_70 + self.def_70

    def _value_at_level(self, fieldname, level=1, is_evolved=False, to_string=True):
        parameter = 0
        if level <= 50:
            parameter = self._para_first_intercept(fieldname, is_evolved) + level * self._para_first_slope(fieldname,
                                                                                                           is_evolved)
        if level > 50:
            parameter = self._para_second_intercept(fieldname, is_evolved) + level * self._para_second_slope(fieldname,
                                                                                                             is_evolved)
        if to_string:
            return int(parameter).__str__()
        return parameter

    # Raw values
    @property
    def max_level(self):
        if self.i_rarity == 0:
            return 50
        else:
            return 70

    @property
    def evolvable(self):
        return (self.i_rarity in EVOLVABLE_RARITIES) and (self.card_type == 0)

    @property
    def is_evolved(self):
        return (False, True)

    # 1-50
    def _para_first_slope(self, fieldname, is_evolved=False):
        if is_evolved:
            # 3 stars
            if self.i_rarity == 2:
                return ((getattr(self, fieldname + '_50') - getattr(self, fieldname + '_1')) / 49.0 +
                        EVOLVED_BONUS_PARAMETER_SLOPE_3_50_DICT[fieldname])
            # 4 stars
            if self.i_rarity == 3:
                return ((getattr(self, fieldname + '_50') - getattr(self, fieldname + '_1')) / 49.0 +
                        EVOLVED_BONUS_PARAMETER_SLOPE_4_50_DICT[fieldname])
        else:
            return (getattr(self, fieldname + '_50') - getattr(self, fieldname + '_1')) / 49.0

    # 51-70
    def _para_second_slope(self, fieldname, is_evolved=False):
        if is_evolved:
            # 3 stars
            if self.i_rarity == 2:
                return ((getattr(self, fieldname + '_70') - getattr(self, fieldname + '_50')) / 20.0 +
                        EVOLVED_BONUS_PARAMETER_SLOPE_3_70_DICT[fieldname])
            # 4 stars
            if self.i_rarity == 3:
                return ((getattr(self, fieldname + '_70') - getattr(self, fieldname + '_50')) / 20.0 +
                        EVOLVED_BONUS_PARAMETER_SLOPE_4_70_DICT[fieldname])
        return (getattr(self, fieldname + '_70') - getattr(self, fieldname + '_50')) / 20.0

    # 1-50
    def _para_first_intercept(self, fieldname, is_evolved=False):
        if is_evolved:
            # 3 stars
            if self.i_rarity == 2:
                return (getattr(self, fieldname + '_1') - self._para_first_slope(fieldname) +
                        EVOLVED_BONUS_PARAMETER_INTERCEPT_3_50_DICT[fieldname])
            # 4 stars
            if self.i_rarity == 3:
                return (getattr(self, fieldname + '_1') - self._para_first_slope(fieldname) +
                        EVOLVED_BONUS_PARAMETER_INTERCEPT_4_50_DICT[fieldname])
        return getattr(self, fieldname + '_1') - self._para_first_slope(fieldname, False)

    # 51-70
    def _para_second_intercept(self, fieldname, is_evolved=False):
        if is_evolved:
            # 3 stars
            if self.i_rarity == 2:
                return (getattr(self, fieldname + '_50') - 50 * self._para_second_slope(fieldname) +
                        EVOLVED_BONUS_PARAMETER_INTERCEPT_3_70_DICT[fieldname])
            # 4 stars
            if self.i_rarity == 3:
                return (getattr(self, fieldname + '_50') - 50 * self._para_second_slope(fieldname) +
                        EVOLVED_BONUS_PARAMETER_INTERCEPT_4_70_DICT[fieldname])
        return getattr(self, fieldname + '_50') - 50 * self._para_second_slope(fieldname, False)

    # Action skill
    skill_name = models.CharField(_('Skill name'), max_length=100)
    japanese_skill_name = models.CharField(string_concat(_('Skill name'), ' (', t['Japanese'], ')'), max_length=100)
    skill_SP = models.PositiveIntegerField(_('Skill SP'), default=0)
    skill_combo = models.PositiveIntegerField(_('Skill combo'), default=0)
    skill_hits = models.PositiveIntegerField(_('Skill hits'), default=0)

    skill_damage = models.CharField(_('Skill damage'), max_length=300)
    skill_range = models.CharField(_('Skill range'), max_length=300)
    skill_comment = models.CharField(_('Skill comment'), max_length=1000)

    max_damage = models.PositiveIntegerField(_('Max damage'), default=0)

    ############## EFFECTS ################

    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################

    # Nakayoshi
    nakayoshi_skills = models.ManyToManyField('Nakayoshi', related_name='card_with_nakayoshi')
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################


############################################################
# Weapons

class Weapon(ItemModel):
    collection_name = 'weapon'

    owner = models.ForeignKey(User, related_name='added_weapons')
    name = models.CharField(_('Name'), max_length=100)

    def __unicode__(self):
        return self.name

    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    image = models.ImageField(_('Icon'), upload_to=uploadItem('w'))
    rhythm = models.ImageField(_('Rhythm'), upload_to=uploadItem('w/rhythm'))
    i_weapon = models.PositiveIntegerField(_('Weapon'), choices=WEAPON_CHOICES)

    @property
    def weapon(self):
        return WEAPON_DICT[self.i_weapon]

    @property
    def english_weapon(self):
        return ENGLISH_WEAPON_DICT[self.i_weapon]


############################################################
# Weapon variations

class WeaponUpgrade(ItemModel):
    collection_name = 'weapon_upgrade'

    origin = models.ForeignKey(Weapon, verbose_name=_('Weapon'), related_name='upgrade', null=True,
                               on_delete=models.SET_NULL)

    level = models.PositiveIntegerField(_('Upgrade Level'), choices=UPGRADE_LEVEL_CHOICES, default=0)

    def __unicode__(self):
        return self.origin.name + self.level.__str__()

    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=RARITY_CHOICES, default=0)

    @property
    def rarity(self):
        return RARITY_DICT[self.i_rarity]

    atk_min = models.PositiveIntegerField(string_concat(_('Weapon ATK'), ' (', _('Minimum'), ')'), default=0)
    atk_max = models.PositiveIntegerField(string_concat(_('Weapon ATK'), ' (', _('Maximum'), ')'), default=0)

    def _atk_at_level(self, level=1, to_string=True):
        atk_value = self.atk_min + (level - 1) * (self.atk_max - self.atk_min) / 49
        if to_string:
            return int(atk_value).__str__()
        return atk_value

    price = models.PositiveIntegerField(_('Price'), default=0)

    # Materials
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################

    # Skills
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################

    # Subskill
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################


############################################################
# Nakayoshi

class Nakayoshi(ItemModel):
    collection_name = 'nakayoshi'

    i_name = models.PositiveIntegerField(_('Nakayoshi skill'), choices=NAKAYOSHI_SKILLS_CHOICES,
                                         null=True)

    # Get bonus value
    positive_effect = models.BooleanField(_('Positive Effect'), default=True)
    effect_level = models.PositiveIntegerField(_('Effect level'), null=True, blank=True,
                                               choices=ENGLISH_SKILL_SIZE_CHOICES, default=None)

    @property
    def nakayoshi_skill(self):
        if self.i_name is not None:
            return NAKAYOSHI_SKILLS_DICT[self.i_name]
        else:
            return None

    @property
    def english_nakayoshi_skill(self):
        if self.i_name is not None:
            return ENGLISH_NAKAYOSHI_SKILLS_DICT[self.i_name]
        else:
            return None

    @property
    def auto_bonus_value(self):
        if self.effect_level is not None:
            return SKILL_SIZE_VALUE_DICT[self.english_nakayoshi_skill][self.effect_level]
        else:
            return None

    bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True, default=auto_bonus_value)

############################################################
# Stages
class Stage(ItemModel):
    collection_name = 'stage'

    name = models.CharField(_('Stage'), null=True, max_length=50)
    episode = models.PositiveIntegerField(_('Episode'), null=True)
    number = models.PositiveIntegerField(_('Stage number'), null=True)

    # Materials
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################

    # Irousu
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################
    #####################

############################################################
# Stages
class StageDifficulty(ItemModel):
    collection_name = 'stage_dificulty'
    collection_plural_name = 'stage_dificulties'

    stage = models.ForeignKey(Stage, verbose_name=_('Stage'), related_name='difficulties', null=True,
                               on_delete=models.SET_NULL)
    difficulty = models.PositiveIntegerField(_('Difficulty'), null=True, choices=DIFFICULTY_CHOICES)
    level = models.PositiveIntegerField(_('Level'), null=True)

    exp = models.PositiveIntegerField(_('EXP'), null=True)
    coins = models.PositiveIntegerField(_('Coins'), null=True)
    cheerpoints = models.PositiveIntegerField(_('Cheerpoints'), null=True)

    objectives = models.CharField(_('Objectives'), max_length=200)

############################################################
# Materials


############################################################
# Irousu

class Irousu(ItemModel):
    collection_name = 'irousu'



############################################################
# Events
