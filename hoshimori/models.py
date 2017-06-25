# -*- coding: utf-8 -*-
from __future__ import division

import datetime
import os

from django.conf import settings as django_settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from magi.item_model import MagiModel, get_image_url_from_path, get_http_image_url_from_path
from magi.models import User
from magi.utils import tourldash, randomString, AttrDict
from multiselectfield import MultiSelectField

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

class Student(MagiModel):
    collection_name = 'student'

    name = models.CharField(_('Name'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    unlock = models.CharField(_('Unlock at'), max_length=100)

    owner = models.ForeignKey(User, related_name='added_students')

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
    ideal_1 = models.CharField(_('Ideal model 1'), max_length=100)
    ideal_2 = models.CharField(_('Ideal model 2'), max_length=100)
    ideal_3 = models.CharField(_('Ideal model 3'), max_length=100)
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
    def http_full_image_url(self):
        return get_http_image_url_from_path(self.full_image)

    # Full body images
    signature = models.ImageField(_('Signature'), upload_to=uploadItem('s/sign'))

    @property
    def signature_url(self):
        return get_image_url_from_path(self.signature)

    @property
    def http_signature_url(self):
        return get_http_image_url_from_path(self.signature)

    # Voices
    phrase_1 = models.FileField(_('Phrase 1'), upload_to=uploadItem('s/voices'))
    phrase_2 = models.FileField(_('Phrase 2'), upload_to=uploadItem('s/voices'))
    introduction_1 = models.FileField(_('Introduction 1'), upload_to=uploadItem('s/voices'))
    introduction_2 = models.FileField(_('Introduction 1'), upload_to=uploadItem('s/voices'))

    # Actually not images but still can use
    @property
    def phrase_1_url(self):
        return get_image_url_from_path(self.phrase_1)

    @property
    def http_phrase_1_url(self):
        return get_http_image_url_from_path(self.phrase_1)

    @property
    def phrase_2_url(self):
        return get_image_url_from_path(self.phrase_2)

    @property
    def http_phrase_2_url(self):
        return get_http_image_url_from_path(self.phrase_2)

    @property
    def introduction_1_url(self):
        return get_image_url_from_path(self.introduction_1)

    @property
    def http_introduction_1_url(self):
        return get_http_image_url_from_path(self.introduction_1)

    @property
    def introduction_2_url(self):
        return get_image_url_from_path(self.introduction_2)

    @property
    def http_introduction_2_url(self):
        return get_http_image_url_from_path(self.introduction_2)

    # Cache totals
    _cache_totals_days = 2
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)
    _cache_total_events = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_cards = Card.objects.filter(student=self).count()

    def force_cache_totals(self):
        self.update_cache_totals()
        self.save()

    @property
    def cached_total_cards(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(
                hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_cards

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name


############################################################
# Account

class Account(MagiModel):
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

    _cache_owner_days = 20
    _cache_owner_last_update = models.DateTimeField(null=True)
    _cache_owner_username = models.CharField(max_length=32, null=True)
    _cache_owner_email = models.EmailField(null=True)
    _cache_owner_preferences_twitter = models.CharField(max_length=32, null=True)

    def force_cache_owner(self):
        """
        Recommended to use select_related('owner', 'owner__preferences') when calling this method
        """
        self._cache_owner_last_update = timezone.now()
        self._cache_owner_username = self.owner.username
        self._cache_owner_email = self.owner.email
        self._cache_owner_preferences_status = self.owner.preferences.status
        self._cache_owner_preferences_twitter = self.owner.preferences.twitter
        self.save()

    @property
    def cached_owner(self):
        if not self._cache_owner_last_update or self._cache_owner_last_update < timezone.now() - datetime.timedelta(
                days=self._cache_owner_days):
            self.force_cache_owner()
        return AttrDict({
            'pk': self.owner_id,
            'id': self.owner_id,
            'username': self._cache_owner_username,
            'email': self._cache_owner_email,
            'item_url': '/user/{}/{}/'.format(self.owner_id, self._cache_owner_username),
            'preferences': AttrDict({
                'twitter': self._cache_owner_preferences_twitter,
            }),
        })

    def __unicode__(self):
        return u'#{} {} - {}'.format(self.id, self.cached_owner.username, self.nickname)

    def get_cards(self):
        return OwnedCard.objects.filter(account_id=self.id)


############################################################
# Card

class Card(MagiModel):
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

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'), null=True, blank=True)

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
    sp_1 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 1'), ')'), default=0)
    atk_1 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 1'), ')'), default=0)
    def_1 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 1'), ')'), default=0)
    hp_50 = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Level 50'), ')'), default=0)
    sp_50 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 50'), ')'), default=0)
    atk_50 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 50'), ')'), default=0)
    def_50 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 50'), ')'), default=0)
    hp_70 = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Level 70'), ')'), default=0, null=True)
    sp_70 = models.PositiveIntegerField(string_concat(_('SP'), ' (', _('Level 70'), ')'), default=0, null=True)
    atk_70 = models.PositiveIntegerField(string_concat(_('ATK'), ' (', _('Level 70'), ')'), default=0, null=True)
    def_70 = models.PositiveIntegerField(string_concat(_('DEF'), ' (', _('Level 70'), ')'), default=0, null=True)

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
    skill_SP = models.PositiveIntegerField(_('Skill SP'), default=0, null=True)
    skill_hits = models.PositiveIntegerField(_('Skill hits'), default=0, null=True)
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

    # TODO: Use String until properly import
    # action_skill = models.OneToOne('ActionSkill', verbose_name=_('Action Skill'), related_name='skill', null=True,
    #                                  on_delete=models.SET_NULL)
    # evolved_action_skill = models.OneToOne('ActionSkill', verbose_name=_('Evolved Action Skill'),
    #                                          related_name='evolved skill', null=True, on_delete=models.SET_NULL)
    action_skill_damage = models.CharField(_('Skill Damage'), max_length=200)
    action_skill_combo = models.PositiveIntegerField(_('Skill Combo'), default=13, null=True)
    action_skill_effects = models.CharField(_('Skill Effect'), max_length=200)
    evolved_action_skill_damage = models.CharField(string_concat(_('Skill Damage'), ' (', _('Evolved'), ')'),
                                                   max_length=200)
    evolved_action_skill_combo = models.PositiveIntegerField(string_concat(_('Skill Combo'), ' (', _('Evolved'), ')'),
                                                             default=13, null=True)
    evolved_action_skill_effects = models.CharField(string_concat(_('Skill Effect'), ' (', _('Evolved'), ')'),
                                                    max_length=200)

    # Nakayoshi
    nakayoshi_title = models.CharField(_('Passive Skill'), max_length=100)
    japanese_nakayoshi_title = models.CharField(string_concat(_('Passive Skill'), ' (', t['Japanese'], ')'),
                                                max_length=100)

    # TODO: Use String until properly import
    # nakayoshi_skills = models.ManyToManyField('Nakayoshi', related_name='card_with_nakayoshi')
    # evolved_nakayoshi_skills = models.ManyToManyField('Nakayoshi', related_name='card_with_nakayoshi_evolved',
    #                                                   null=True, default=None)

    nakayoshi_skill_effect = models.CharField(_('Passive Skill Effect'), max_length=200)
    nakayoshi_skill_target = models.CharField(_('Passive Skill Target'), max_length=200)
    evolved_nakayoshi_skill_effect = models.CharField(string_concat(_('Passive Skill Effect'), ' (', _('Evolved'), ')'),
                                                      max_length=200)
    evolved_nakayoshi_skill_target = models.CharField(string_concat(_('Passive Skill Target'), ' (', _('Evolved'), ')'),
                                                      max_length=200)

    # Charge attack
    charge_name = models.CharField(_('Charge name'), max_length=100)
    charge_hit = models.PositiveIntegerField(_('Charge hits'), null=True)
    charge_damage = models.CharField(_('Charge damage'), max_length=200)
    charge_range = models.CharField(_('Charge range'), max_length=300)
    charge_comment = models.CharField(_('Charge comment'), max_length=1000)

    # Cache student

    _cache_student_days = 20
    _cache_student_last_update = models.DateTimeField(null=True)
    _cache_student_name = models.CharField(max_length=100, null=True)
    _cache_student_japanese_name = models.CharField(max_length=100, null=True)
    _cache_student_image = models.ImageField(upload_to=uploadItem('cache_student'), null=True)

    def update_cache_student(self):
        self._cache_student_last_update = timezone.now()
        self._cache_student_name = self.student.name
        self._cache_student_japanese_name = self.student.japanese_name
        self._cache_student_image = self.student.image

    def force_cache_student(self):
        self.update_cache_student()
        self.save()

    @property
    def cached_student(self):
        if not self._cache_student_last_update or self._cache_student_last_update < timezone.now() - datetime.timedelta(
                days=self._cache_student_days):
            self.force_cache_student()
        return AttrDict({
            'pk': self.student_id,
            'id': self.student_id,
            'unicode': self._cache_student_name if get_language() != 'ja' else self._cache_student_japanese_name,
            'name': self._cache_student_name,
            'japanese_name': self._cache_student_japanese_name,
            'image': self._cache_student_image,
            'image_url': get_image_url_from_path(self._cache_student_image),
            'http_image_url': get_http_image_url_from_path(self._cache_student_image),
            'item_url': u'/student/{}/{}/'.format(self.student_id, tourldash(self._cache_student_name)),
            'ajax_item_url': u'/ajax/student/{}/'.format(self.student_id),
        })

    # Cache totals
    _cache_totals_days = 2
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_owners = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_owners = User.objects.filter(accounts__ownedcards__card=self).distinct().count()

    def force_cache_totals(self):
        self.update_cache_totals()
        self.save()

    @property
    def cached_total_owners(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(
                hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_owners

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        else:
            return self.name


############################################################
# Action Skill

# class ActionSkill(MagiModel):
#     collection_name = 'action_skill'
#
#     name = models.CharField(_('Action Skill'), max_length=100)
#     japanese_name = models.CharField(string_concat(_('Action Skill'), ' (', t['Japanese'], ')'), max_length=100)
#
#     def __unicode__(self):
#         if get_language() == 'ja':
#             return self.japanese_name
#         else:
#             return self.name
#
#     damage = models.CharField(_('Skill Damage'), max_length=200)
#     combo = models.PositiveIntegerField(_('Skill Combo'), default=13)
#     effects = models.ManyToManyField('ActionSkillEffect', related_name='skills_with_effect', null=True)


############################################################
# Action Skill Effect

# class ActionSkillEffect(MagiModel):
#     collection_name = 'action_skill_effect'
#
#     i_name = models.CharField(_('Action Skill Effect'), max_length=100)
#
#     bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)
#     duration = models.PositiveIntegerField(_('Effect Duration'), null=True)
#     skill_affinity = models.PositiveIntegerField(_('Skill Affinity'), null=True, choices=SKILL_AFFINITY_CHOICES,
#                                                  default=IGNORE_AFFINITY)
#
#     def __unicode__(self):
#         return '{} {}'.format(self.i_name, self.bonus_value)


############################################################
# Weapons

class Weapon(MagiModel):
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

    def get_upgrades(self):
        return self.weapon_with_upgrades.all()


############################################################
# Weapon variations

class WeaponUpgrade(MagiModel):
    collection_name = 'weapon_upgrade'

    origin = models.ForeignKey(Weapon, verbose_name=_('Weapon'), related_name='weapon_with_upgrades', null=True,
                               on_delete=models.SET_NULL)

    def owner(self):
        return self.origin

    def owner_id(self):
        return self.origin_id

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

    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=WEAPON_RARITY_CHOICES, default=0)

    @property
    def rarity(self):
        return WEAPON_RARITY_DICT[self.i_rarity]

    atk_min = models.PositiveIntegerField(string_concat(_('Weapon ATK'), ' (', _('Minimum'), ')'), default=0)
    atk_max = models.PositiveIntegerField(string_concat(_('Weapon ATK'), ' (', _('Maximum'), ')'), default=0)

    def _atk_at_level(self, level=1, to_string=True):
        atk_value = self.atk_min + (level - 1) * (self.atk_max - self.atk_min) / 49
        if to_string:
            return int(atk_value).__str__()
        return atk_value

    price = models.PositiveIntegerField(_('Price'), default=0)

    # Materials
    materials = models.CharField(_('Material'), null=True, max_length=100)

    # Skills
    # TODO
    # weapon_effects = models.ManyToManyField('WeaponEffect', related_name='weapon_with_skills', null=True)
    weapon_effects = models.CharField(_('Weapon Effects'), max_length=100)

    # Subskill
    # TODO
    # subweapon_effects = models.ManyToManyField('WeaponEffect', related_name='subweapon_with_skills', null=True)
    subweapon_effects = models.CharField(_('Subweapon Effects'), max_length=100)


############################################################
# Weapon skills and subweapon skills

# class WeaponEffect(MagiModel):
#     collection_name = 'weapon_effect'
#
#     i_name = models.PositiveIntegerField(_('Weapon Effect'), choices=WEAPON_EFFECT_CHOICES,
#                                          null=True)
#
#     # Get bonus value
#     positive_effect = models.BooleanField(_('Positive Effect'), default=True)
#     effect_level = models.PositiveIntegerField(_('Effect Level'), null=True)
#     bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)
#
#     @property
#     def weapon_effect(self):
#         if self.i_name is not None:
#             return WEAPON_EFFECT_DICT[self.i_name]
#         else:
#             return None
#
#     @property
#     def english_weapon_effect(self):
#         if self.i_name is not None:
#             return ENGLISH_WEAPON_EFFECT_DICT[self.i_name]
#         else:
#             return None
#
#     def __unicode__(self):
#         if self.positive_effect:
#             return '{} +{}'.format(self.english_weapon_effect, self.bonus_value)
#         else:
#             return '{} -{}'.format(self.english_weapon_effect, self.bonus_value)


############################################################
# Nakayoshi

# class Nakayoshi(MagiModel):
#     collection_name = 'nakayoshi'
#
#     effect_name = models.PositiveIntegerField(_('Nakayoshi skill'), choices=NAKAYOSHI_SKILL_CHOICES,
#                                               null=True)
#
#     # Get bonus value
#     positive_effect = models.BooleanField(_('Positive Effect'), default=True)
#     effect_level = models.PositiveIntegerField(_('Effect Level'), null=True, blank=True,
#                                                choices=ENGLISH_SKILL_SIZE_CHOICES)
#
#     bonus_value = models.PositiveIntegerField(_('Effect Value'), null=True)
#
#     @property
#     def nakayoshi_skill_name(self):
#         if self.effect_name is not None:
#             return NAKAYOSHI_SKILL_DICT[self.effect_name]
#         else:
#             return None
#
#     @property
#     def english_nakayoshi_skill_name(self):
#         if self.effect_name is not None:
#             return ENGLISH_NAKAYOSHI_SKILL_DICT[self.effect_name]
#         else:
#             return None
#
#     def __unicode__(self):
#         if self.positive_effect:
#             return '{} +{}'.format(self.english_nakayoshi_skill_name, self.bonus_value)
#         else:
#             return '{} -{}'.format(self.english_nakayoshi_skill_name, self.bonus_value)


############################################################
# Stages

class Stage(MagiModel):
    collection_name = 'stage'

    owner = models.ForeignKey(User, related_name='added_stages')

    name = models.CharField(_('Stage'), max_length=50)
    part = models.CharField(_('Part'), null=True, max_length=50)
    episode = models.PositiveIntegerField(_('Episode'), null=True)
    number = models.PositiveIntegerField(_('Stage number'), null=True)

    # Materials
    materials = models.CharField('Material', null=True, max_length=100)

    def get_drops(self):
        return self.materials.split(chr(10))

    # Irous
    small_irous = models.ManyToManyField('IrousVariation', related_name='stage_with_small_irous', null=True)
    large_irous = models.ManyToManyField('IrousVariation', related_name='stage_with_large_irous', null=True)

    def get_small_irous(self):
        return self.small_irous.all()

    def get_large_irous(self):
        return self.large_irous.all()

    easy_stage = models.OneToOneField('StageDifficulty', related_name='easy_difficulty')
    normal_stage = models.OneToOneField('StageDifficulty', related_name='normal_difficulty')
    hard_stage = models.OneToOneField('StageDifficulty', related_name='hard_difficulty')

    def __unicode__(self):
        return '{} - {}'.format(self.episode, self.number)

    @property
    def next_stage(self):
        # If last stage
        try:
            if self.number == 4:
                return Stage.objects.get(episode=self.episode + 1, number=1)
            else:
                return Stage.objects.get(episode=self.episode, number=self.number + 1)
        except ObjectDoesNotExist:
            return None

    @property
    def prev_stage(self):
        try:
            # If first stage
            if self.number == 1:
                return Stage.objects.get(episode=self.episode - 1, number=4)
            else:
                return Stage.objects.get(episode=self.episode, number=self.number - 1)
        except ObjectDoesNotExist:
            return None


############################################################
# Stages

class StageDifficulty(MagiModel):
    collection_name = 'stage_dificulty'
    collection_plural_name = 'stage_dificulties'

    difficulty = models.PositiveIntegerField(_('Difficulty'), null=True, choices=DIFFICULTY_CHOICES)
    level = models.PositiveIntegerField(_('Level'), null=True)

    exp = models.PositiveIntegerField(_('EXP'), null=True)
    coins = models.PositiveIntegerField(_('Coins'), null=True)
    cheerpoints = models.PositiveIntegerField(_('Cheerpoints'), null=True)

    objectives = models.CharField(_('Objectives'), max_length=200)

    def get_objectives(self):
        return self.objectives.split(chr(10))

    # def stage(self):
    #     if self.easy_difficulty is not None:
    #         return self.easy_difficulty
    #     if self.difficulty == NORMAL and self.normal_difficulty is not None:
    #         return self.normal_difficulty
    #     if self.difficulty == HARD and self.hard_difficulty is not None:
    #         return self.hard_difficulty
    #     else:
    #         return None

    def __unicode__(self):
        # if self.stage():
        #     return '{} - {} {}'.format(self.stage().episode, self.stage().number, DIFFICULTY_DICT[self.difficulty])
        # else:
        return '#{} {}'.format(self.id, DIFFICULTY_DICT[self.difficulty])


############################################################
# Materials

# class Material(MagiModel):
#     collection_name = 'material'
#
#     name = models.CharField(_('Material name'), unique=True, max_length=50)
#
#     def __unicode__(self):
#         return self.name


############################################################
# Irous

class Irous(MagiModel):
    collection_name = 'irous'

    name = models.PositiveIntegerField(_('Irous type'), choices=IROUS_TYPE_CHOICES, null=True, unique=True)

    weak = MultiSelectField(_('Weak'), choices=WEAPON_CHOICES, max_length=100, default="")
    strong = MultiSelectField(_('Strong'), choices=WEAPON_CHOICES, max_length=100, default="")
    guard = MultiSelectField(_('Guard'), choices=WEAPON_CHOICES, max_length=100, default="")

    def english_name(self):
        return ENGLISH_IROUS_TYPE_DICT[self.name]

    def owner(self):
        return self

    def owner_id(self):
        return self.id

    def __unicode__(self):
        return self.english_name()


############################################################
# Irous variations

class IrousVariation(MagiModel):
    collection_name = 'irousvariation'

    name = models.CharField(_('Irous Name'), unique=True, max_length=50)
    japanese_name = models.CharField(string_concat(_('Irous Name'), ' (', t['Japanese'], ')'), max_length=50)

    species = models.ForeignKey(Irous, related_name='species', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    is_large_irous = models.BooleanField(_('Large Irous'), default = True)

    def owner(self):
        return self.species

    def owner_id(self):
        return self.species_id

    def __unicode__(self):
        return '{} - {}'.format(ENGLISH_IROUS_TYPE_DICT[self.species.name], self.name)

    def get_stages(self):
        if self.is_large_irous:
            return Stage.objects.filter(large_irous=self.id)
        else:
            return Stage.objects.filter(small_irous=self.id)


############################################################
# Events

class Event(MagiModel):
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

class OwnedCard(MagiModel):
    collection_name = 'ownedcard'

    account = models.ForeignKey(Account, related_name='ownedcards', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='owned', on_delete=models.CASCADE)
    evolved = models.BooleanField(_('Evolved'), default=False)
    level = models.PositiveIntegerField(_('Level'), default=70, validators=[
        MinValueValidator(1),
        MaxValueValidator(70),
    ])

    obtained_date = models.DateField(_('Obtained Date'), null=True, blank=True)

    # Cache account + owner
    _cache_account_days = 200
    _cache_account_last_update = models.DateTimeField(null=True)
    _cache_account_owner_id = models.PositiveIntegerField(null=True)

    def update_cache_account(self):
        self._cache_account_last_update = timezone.now()
        self._cache_account_owner_id = self.account.owner_id

    def force_cache_account(self):
        self.update_cache_account()
        self.save()

    @property
    def cached_account(self):
        if not self._cache_account_last_update or self._cache_account_last_update < timezone.now() - datetime.timedelta(
                days=self._cache_account_days):
            self.force_cache_account()
        return AttrDict({
            'pk': self.account_id,
            'id': self.account_id,
            'owner': AttrDict({
                'id': self._cache_account_owner_id,
                'pk': self._cache_account_owner_id,
            }),
        })

    @property
    def owner(self):
        return self.cached_account.owner

    @property
    def owner_id(self):
        return self.cached_account.owner.id

    def __unicode__(self):
        return u'#{} {} {}'.format(self.id, self.card.name, u'({})'.format(_('Evolved')) if self.evolved else '')


############################################################
# Favorite Card

class FavoriteCard(MagiModel):
    collection_name = 'favoritecard'

    owner = models.ForeignKey(User, related_name='favoritecards')
    card = models.ForeignKey(Card, related_name='senseis', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'#{}'.format(self.card.id)

    class Meta:
        unique_together = (('owner', 'card'),)
