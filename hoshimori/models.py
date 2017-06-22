# -*- coding: utf-8 -*-
from __future__ import division

import os

from django.conf import settings as django_settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from multiselectfield import MultiSelectField
from web.item_model import ItemModel, get_image_url_from_path, get_http_image_url_from_path
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

    name = models.CharField(_('Name'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    unlock = models.CharField(_('Unlock at'), max_length=100)

    owner = models.ForeignKey(User, related_name='added_students')

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name

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

    CV = models.CharField(string_concat(_('CV'), ' (', t['Japanese'], ')'), help_text='In Japanese characters.',
                          max_length=100)
    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100)

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('s'))

    @property
    def image_url(self):
        return get_image_url_from_path(self.image)

    @property
    def http_image_url(self):
        return get_http_image_url_from_path(self.image)

    # Full body images
    full_image = models.ImageField(_('Full Body Image'), upload_to=uploadItem('s/full'))

    @property
    def full_image_url(self):
        return get_image_url_from_path(self.full_image)

    @property
    def full_http_image_url(self):
        return get_http_image_url_from_path(self.full_image)


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
        return u'#{} {} - {}'.format(self.id, self.owner.get_username(), self.nickname)


############################################################
# Card

class Card(ItemModel):
    collection_name = 'card'

    id = models.AutoField(_('ID'), unique=True, primary_key=True, db_index=True)
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
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100)

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('c'))

    @property
    def image_url(self):
        return get_image_url_from_path(self.image)

    @property
    def http_image_url(self):
        return get_http_image_url_from_path(self.image)

    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'), null=True)

    @property
    def art_url(self):
        return get_image_url_from_path(self.art)

    @property
    def http_art_url(self):
        return get_http_image_url_from_path(self.art)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'), null=True)

    @property
    def transparent_url(self):
        return get_image_url_from_path(self.transparent)

    @property
    def http_transparent_url(self):
        return get_http_image_url_from_path(self.transparent)

    # Sub card effect
    subcard_effect = models.BooleanField(_('Subcard Effect'), default=False)

    # Card type
    card_type = models.PositiveIntegerField(_('Card Type'), choices=CARDTYPE_CHOICES, default=0)

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
    skill_hits = models.PositiveIntegerField(_('Skill hits'), default=0)
    skill_range = models.CharField(_('Skill range'), max_length=300)
    skill_comment = models.CharField(_('Skill comment'), max_length=1000)
    skill_preview = models.ImageField(_('Skill preview'), upload_to=uploadItem('c/skill'), null=True)

    @property
    def skill_preview_url(self):
        return get_image_url_from_path(self.skill_preview)

    @property
    def http_skill_preview_url(self):
        return get_http_image_url_from_path(self.skill_preview)

    max_damage = models.PositiveIntegerField(_('Max damage'), default=0)

    action_skill = models.ForeignKey('ActionSkill', verbose_name=_('Action Skill'), related_name='skill', null=True,
                                     on_delete=models.SET_NULL)
    evolved_action_skill = models.ForeignKey('ActionSkill', verbose_name=_('Evolved Action Skill'),
                                             related_name='evolved skill', null=True, on_delete=models.SET_NULL)

    # Nakayoshi
    nakayoshi_title = models.CharField(_('Passive Skill'), max_length=100)
    japanese_nakayoshi_title = models.CharField(string_concat(_('Passive Skill'), ' (', t['Japanese'], ')'),
                                                max_length=100)
    nakayoshi_skills = models.ManyToManyField('Nakayoshi', related_name='card_with_nakayoshi')
    evolved_nakayoshi_skills = models.ManyToManyField('Nakayoshi', related_name='card_with_nakayoshi_evolved',
                                                      null=True, default=None)

    # Charge attack
    charge_name = models.CharField(_('Charge name'), max_length=100, null=True)
    charge_hit = models.PositiveIntegerField(_('Charge hits'), null=True)
    charge_damage = models.CharField(_('Charge Damage'), max_length=200, null=True)
    charge_range = models.CharField(_('Charge range'), max_length=300, null=True)
    charge_comment = models.CharField(_('Charge comment'), max_length=1000, null=True)


############################################################
# Action Skill
class ActionSkill(ItemModel):
    collection_name = 'action_skill'

    name = models.CharField(_('Action Skill'), max_length=100)
    japanese_name = models.CharField(string_concat(_('Action Skill'), ' (', t['Japanese'], ')'), max_length=100)

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name

    damage = models.CharField(_('Skill Damage'), max_length=200)
    combo = models.PositiveIntegerField(_('Skill Combo'), default=13)
    effects = models.ManyToManyField('ActionSkillEffect', related_name='skills_with_effect', null=True)


############################################################
# Action Skill Effect

class ActionSkillEffect(ItemModel):
    collection_name = 'action_skill_effect'

    i_name = models.CharField(_('Action Skill Effect'), max_length=100)

    bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)
    duration = models.PositiveIntegerField(_('Effect Duration'), null=True)
    skill_affinity = models.PositiveIntegerField(_('Skill Affinity'), null=True, choices=SKILL_AFFINITY_CHOICES,
                                                 default=IGNORE_AFFINITY)

    def __unicode__(self):
        return '{} {}'.format(self.i_name, self.bonus_value)


############################################################
# Weapons

class Weapon(ItemModel):
    collection_name = 'weapon'

    name = models.CharField(_('Name'), max_length=100)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name

    image = models.ImageField(_('Icon'), upload_to=uploadItem('w'))
    i_type = models.PositiveIntegerField(_('Weapon'), choices=WEAPON_CHOICES)

    @property
    def type(self):
        return WEAPON_DICT[self.i_type]

    @property
    def english_type(self):
        return ENGLISH_WEAPON_DICT[self.i_type]


############################################################
# Weapon variations

class WeaponUpgrade(ItemModel):
    collection_name = 'weapon_upgrade'

    owner = models.ForeignKey(User, related_name='added_weapons')
    origin = models.ForeignKey(Weapon, verbose_name=_('Weapon'), related_name='upgrade', null=True,
                               on_delete=models.SET_NULL)

    rhythm = models.ImageField(_('Rhythm'), upload_to=uploadItem('w/rhythm'))
    i_level = models.PositiveIntegerField(_('Upgrade Level'), choices=UPGRADE_LEVEL_CHOICES, null=True, default=0)
    gamma_type = models.CharField(_('Gamma Type'), max_length=1, default='')

    @property
    def upgrade_level(self):
        return UPGRADE_LEVEL_DICT[self.i_level]

    @property
    def english_upgrade_level(self):
        return ENGLISH_UPGRADE_LEVEL_DICT[self.i_level]

    def __unicode__(self):
        if get_language() == 'ja':
            return u'{} {} {}'.format(str(self.origin.japanese_name), self.english_upgrade_level, self.gamma_type)
        else:
            return u'{} {} {}'.format(str(self.origin.name), self.english_upgrade_level, self.gamma_type)

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
    materials = models.CharField('Material', null=True, max_length=100)

    # Skills
    weapon_effects = models.ManyToManyField('WeaponEffect', related_name='weapon_with_skills', null=True)

    # Subskill
    subweapon_effects = models.ManyToManyField('WeaponEffect', related_name='subweapon_with_skills', null=True)


############################################################
# Weapon skills and subweapon skills

class WeaponEffect(ItemModel):
    collection_name = 'weapon_effect'

    i_name = models.PositiveIntegerField(_('Weapon Effect'), choices=WEAPON_EFFECT_CHOICES,
                                         null=True)

    # Get bonus value
    positive_effect = models.BooleanField(_('Positive Effect'), default=True)
    effect_level = models.PositiveIntegerField(_('Effect Level'), null=True)
    bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)

    @property
    def weapon_effect(self):
        if self.i_name is not None:
            return WEAPON_EFFECT_DICT[self.i_name]
        else:
            return None

    @property
    def english_weapon_effect(self):
        if self.i_name is not None:
            return ENGLISH_WEAPON_EFFECT_DICT[self.i_name]
        else:
            return None

    def __unicode__(self):
        if self.positive_effect:
            return '{} +{}'.format(self.english_weapon_effect, self.bonus_value)
        else:
            return '{} -{}'.format(self.english_weapon_effect, self.bonus_value)


############################################################
# Nakayoshi

class Nakayoshi(ItemModel):
    collection_name = 'nakayoshi'

    i_name = models.PositiveIntegerField(_('Nakayoshi skill'), choices=NAKAYOSHI_SKILL_CHOICES,
                                         null=True)

    # Get bonus value
    positive_effect = models.BooleanField(_('Positive Effect'), default=True)
    effect_level = models.PositiveIntegerField(_('Effect Level'), null=True, blank=True,
                                               choices=ENGLISH_SKILL_SIZE_CHOICES)

    bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)

    @property
    def nakayoshi_skill(self):
        if self.i_name is not None:
            return NAKAYOSHI_SKILL_DICT[self.i_name]
        else:
            return None

    @property
    def english_nakayoshi_skill(self):
        if self.i_name is not None:
            return ENGLISH_NAKAYOSHI_SKILL_DICT[self.i_name]
        else:
            return None

    def __unicode__(self):
        if self.positive_effect:
            return '{} +{}'.format(self.english_nakayoshi_skill, self.bonus_value)
        else:
            return '{} -{}'.format(self.english_nakayoshi_skill, self.bonus_value)


############################################################
# Stages

class Stage(ItemModel):
    collection_name = 'stage'

    owner = models.ForeignKey(User, related_name='added_stages')

    name = models.CharField(_('Stage'), max_length=50)
    part = models.CharField(_('Part'), null=True, max_length=50)
    episode = models.PositiveIntegerField(_('Episode'), null=True)
    number = models.PositiveIntegerField(_('Stage number'), null=True)

    # Materials
    materials = models.CharField('Material', null=True, max_length=100)

    # Irousu
    small_irousu = models.ManyToManyField('IrousuVariation', related_name='stage_with_small_irousu', null=True)
    large_irousu = models.ManyToManyField('IrousuVariation', related_name='stage_with_large_irousu', null=True)

    easy_stage = models.ForeignKey('StageDifficulty', related_name='easy_difficulty')
    normal_stage = models.ForeignKey('StageDifficulty', related_name='normal_difficulty')
    hard_stage = models.ForeignKey('StageDifficulty', related_name='hard_difficulty')

    def __unicode__(self):
        return '{} - {}'.format(self.episode, self.number)


############################################################
# Stages

class StageDifficulty(ItemModel):
    collection_name = 'stage_dificulty'
    collection_plural_name = 'stage_dificulties'

    stage = models.ForeignKey(Stage, related_name='stage', on_delete=models.CASCADE)
    difficulty = models.PositiveIntegerField(_('Difficulty'), null=True, choices=DIFFICULTY_CHOICES)
    level = models.PositiveIntegerField(_('Level'), null=True)

    exp = models.PositiveIntegerField(_('EXP'), null=True)
    coins = models.PositiveIntegerField(_('Coins'), null=True)
    cheerpoints = models.PositiveIntegerField(_('Cheerpoints'), null=True)

    objectives = models.CharField(_('Objectives'), max_length=200)

    def owner(self):
        return self.stage

    def owner_id(self):
        return self.stage.id

    def __unicode__(self):
        return '{} - {} {}'.format(self.stage.episode, self.stage.number, DIFFICULTY_DICT[self.difficulty])


#
# ############################################################
# # Materials
# class Material(ItemModel):
#     collection_name = 'material'
#
#     name = models.CharField(_('Material name'), unique=True, max_length=50)
#
#     def __unicode__(self):
#         return self.name


############################################################
# Irousu

class Irousu(ItemModel):
    collection_name = 'irousu'

    name = models.PositiveIntegerField(_('Irousu type'), choices=IROUSU_TYPE_CHOICES, null=True, unique=True)

    weak = MultiSelectField(_('Weak'), choices=WEAPON_CHOICES, max_length=100, default="")
    strong = MultiSelectField(_('Strong'), choices=WEAPON_CHOICES, max_length=100, default="")
    guard = MultiSelectField(_('Guard'), choices=WEAPON_CHOICES, max_length=100, default="")

    def __unicode__(self):
        return ENGLISH_IROUSU_TYPE_DICT[self.name]


############################################################
# Irousu variations

class IrousuVariation(ItemModel):
    collection_name = 'irousuvariation'

    name = models.CharField(_('Irousu Name'), unique=True, max_length=50)
    japanese_name = models.CharField(string_concat(_('Irousu Name'), ' (', t['Japanese'], ')'), max_length=50)

    species = models.ForeignKey(Irousu, related_name='species', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))

    def __unicode__(self):
        return '{} - {}'.format(ENGLISH_IROUSU_TYPE_DICT[self.species.name], self.name)


############################################################

# Events
class Event(ItemModel):
    collection_name = 'event'

    owner = models.ForeignKey(User, related_name='added_events')
    image = models.ImageField(_('Image'), upload_to=uploadItem('e'))
    name = models.CharField(_('Name'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, unique=True)
    start_date = models.DateTimeField(_('Beginning'), null=True)
    end_date = models.DateTimeField(_('End'), null=True)

    @property
    def status(self):
        if not self.end_date or not self.start_date:
            return None
        now = timezone.now()
        if now > self.end_date:
            return 'ended'
        elif now > self.start_date:
            return 'current'
        return 'future'

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name


############################################################
# Owned Card

class OwnedCard(ItemModel):
    collection_name = 'ownedcard'

    account = models.ForeignKey(Account, related_name='ownedcards', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='owned', on_delete=models.CASCADE)
    evolved = models.BooleanField(_('Evolved'), default=False)
    level = models.PositiveIntegerField(_('Level'), default=70, validators=[
        MinValueValidator(1),
        MaxValueValidator(70),
    ])

    obtained_date = models.DateField(_('Obtained Date'), null=True, blank=True)

    @property
    def owner(self):
        return self.account.owner

    @property
    def owner_id(self):
        return self.account.owner.id

    def __unicode__(self):
        return u'#{} {} {}'.format(self.id, self.card.name, u'({})'.format(_('Evolved')) if self.evolved else '')


############################################################
# Favorite Card

class FavoriteCard(ItemModel):
    collection_name = 'favoritecard'

    owner = models.ForeignKey(User, related_name='favoritecards')
    card = models.ForeignKey(Card, related_name='fans', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'#{}'.format(self.card.id)

    class Meta:
        unique_together = (('owner', 'card'),)
