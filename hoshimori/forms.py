import datetime
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils.safestring import mark_safe
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms
from web.forms import MagiForm, AutoForm, MagiFiltersForm, MagiFilter
from hoshimori.django_translated import t
from hoshimori import models

# Student
class StudentFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'birthday', 'description']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('birthday', _('Birthday')),
    ]

    class Meta:
        model = models.Student
        fields = ('search', 'i_school_year', 'i_star_sign')

# Card
class CardFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'skill_name', 'japanese_skill_name']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
    ]

    class Meta:
        model = models.Card
        fields = ('search', 'i_rarity', 'i_weapon', 'card_type')

# Weapon
class WeaponFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
    ]

    class Meta:
        model = models.Weapon
        fields = ('search', 'i_type')

# Material
class MaterialFilterForm(MagiFiltersForm):
    search_fields = ['name']

    ordering_fields = [
        ('name', _('Name')),
    ]

    class Meta:
        model = models.Material
        fields = ('search',)
