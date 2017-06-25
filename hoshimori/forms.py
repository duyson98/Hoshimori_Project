from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.forms import MagiFiltersForm, AutoForm, MagiFilter

from hoshimori import models
from hoshimori.model_choices import *
from hoshimori.django_translated import t


############################################################
# Student

class StudentFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'birthday', 'description']

    ordering_fields = [
        ('', _('None')),
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('birthday', _('Birthday')),
        ('height', _('Height')),
        ('weight', _('Weight')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hip', _('Hip')),
    ]

    class Meta:
        model = models.Student
        fields = ('search', 'i_school_year', 'i_star_sign')


############################################################
# Card

class CardForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.previous_student_id = None if self.is_creating else self.instance.student_id
        self.fields['skill_comment'].label = 'Skill comment'

    def save(self, commit=False):
        instance = super(CardForm, self).save(commit=False)
        if self.previous_student_id != instance.student_id:
            instance.update_cache_student()
        if commit:
            instance.save()
        return instance


class CardFilterForm(MagiFiltersForm):
    search_fields = ['_cache_student_name', '_cache_student_japanese_name', 'name', 'japanese_name', 'skill_name',
                     'japanese_skill_name']
    ordering_fields = [
        ('', _('None')),
        ('id', _('ID')),
        ('_cache_student_name', string_concat(_('Student'), ' - ', _('Name'))),
        ('_cache_student_japanese_name', string_concat(_('Student'), ' - ', _('Name'), ' (', t['Japanese'], ')')),
        ('i_rarity', _('Rarity')),
        ('i_weapon', _('Weapon')),
        ('hp_50', string_concat(_('HP'), ' (', _('Level 50'), ')')),
        ('sp_50', string_concat(_('SP'), ' (', _('Level 50'), ')')),
        ('atk_50', string_concat(_('ATK'), ' (', _('Level 50'), ')')),
        ('def_50', string_concat(_('DEF'), ' (', _('Level 50'), ')')),
    ]

    def _evolvable_to_queryset(form, queryset, request, value):
        if value == '2':
            return queryset.filter(i_rarity__in=EVOLVABLE_RARITIES,card_type=0)
        elif value == '3':
            return queryset.exclude(i_rarity__in=EVOLVABLE_RARITIES,card_type=0)
        return queryset

    evolvable = forms.NullBooleanField(initial=None, required=False, label=_('Evolvable'))
    evolvable_filter = MagiFilter(to_queryset=_evolvable_to_queryset)

    card_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + CARDTYPE_CHOICES)

    class Meta:
        model = models.Card
        fields = ('search', 'student', 'card_type', 'i_rarity', 'i_weapon', 'evolvable', 'ordering', 'reverse_order')


############################################################
# Weapon

class WeaponFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    ordering_fields = [
        ('', _('None')),
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
    ]

    class Meta:
        model = models.Weapon
        fields = ('search', 'i_type')


############################################################
# Material

# class MaterialFilterForm(MagiFiltersForm):
#     search_fields = ['name']
#
#     ordering_fields = [
#         ('name', _('Name')),
#     ]
#
#     class Meta:
#         model = models.Material
#         fields = ('search',)

############################################################
# Stage

class StageFilterForm(MagiFiltersForm):
    search_fields = ['name', 'materials']

    ordering_fields = [
        ('', _('None')),
        ('episode', _('Episode')),
        #     ('easy_level', _('Easy Level')),
        #     ('easy_exp', _('Easy EXP')),
        #     ('easy_coins', _('Easy Coins')),
        #     ('easy_cheerpoint', _('Easy Cheerpoints')),
        #     ('normal_level', _('Normal Level')),
        #     ('normal_exp', _('Normal EXP')),
        #     ('normal_coins', _('Normal Coins')),
        #     ('normal_cheerpoint', _('Normal Cheerpoints')),
        #     ('hard_level', _('Hard Level')),
        #     ('hard_exp', _('Hard EXP')),
        #     ('hard_coins', _('Hard Coins')),
        #     ('hard_cheerpoint', _('Hard Cheerpoints')),
    ]

    class Meta:
        model = models.Stage
        fields = ('search', 'part')


############################################################
# Irousu Variation

class IrousuVariationFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    class Meta:
        model = models.IrousuVariation
        fields = ('search', 'species', "is_large_irousu")
