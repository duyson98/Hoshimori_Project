import datetime

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.forms import MagiFiltersForm, AutoForm, MagiFilter

from hoshimori import models
from hoshimori.django_translated import t
from hoshimori.model_choices import *

class FormSaveOwnerOnCreation(AutoForm):
    def save(self, commit=True):
        instance = super(FormSaveOwnerOnCreation, self).save(commit=False)
        if self.is_creating:
            instance.owner = self.request.user
        if commit:
            instance.save()
        return instance

############################################################
# Account

class AccountFilterForm(MagiFiltersForm):
    search_fields = ['owner', 'nickname', 'game_id', 'device']

    os = forms.ChoiceField(choices=BLANK_CHOICE_DASH + OS_CHOICES, label=_('Operating System'))
    player_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + PLAYERTYPE_CHOICES, label=_('Player Type'))


    class Meta:
        model = models.Account
        fields = ('search', 'os', 'player_type')

############################################################
# Student

class StudentForm(FormSaveOwnerOnCreation):
    class Meta:
        model = models.Student
        fields = (
            'name', 'japanese_name', 'i_school_year', 'unlock', 'birthday', 'height', 'weight', 'i_blood_type', 'bust',
            'waist', 'hip', 'i_star_sign', 'extra_activity', 'catchphrase_1', 'catchphrase_2', 'height', 'weight',
            'bust', 'waist', 'hip', 'hobby_1', 'hobby_2', 'hobby_3', 'food_likes', 'food_dislikes', 'family', 'dream',
            'ideal_1', 'ideal_2', 'ideal_3', 'pastime', 'destress', 'fav_memory', 'fav_phrase', 'secret', 'CV',
            'romaji_CV', 'image', 'full_image')
        optional_fields = (
            'japanese_name', 'i_school_year', 'unlock', 'birthday', 'height', 'weight', 'i_blood_type', 'bust', 'waist',
            'hip', 'i_star_sign', 'extra_activity', 'catchphrase_1', 'catchphrase_2', 'height', 'weight', 'bust',
            'waist', 'hip', 'hobby_1', 'hobby_2', 'hobby_3', 'food_likes', 'food_dislikes', 'family', 'dream',
            'ideal_1', 'ideal_2', 'ideal_3', 'pastime', 'destress', 'fav_memory', 'fav_phrase', 'secret', 'CV',
            'romaji_CV', 'full_image')
        date_fields = ('birthday',)


class StudentFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'CV', 'romaji_CV']

    ordering_fields = [
        ('id', _('ID')),
        ('name', _('Name')),
        ('birthday', _('Birthday')),
        ('height', _('Height')),
        ('weight', _('Weight')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hip', _('Hip')),
    ]

    def __init__(self, *args, **kwargs):
        super(StudentFilterForm, self).__init__(*args, **kwargs)
        self.fields['reverse_order'].initial = False


    class Meta:
        model = models.Student
        fields = ('search', 'i_school_year', 'i_blood_type', 'i_star_sign', 'ordering', 'reverse_order')


############################################################
# Card

class CardForm(FormSaveOwnerOnCreation):
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.previous_student_id = None
        if hasattr(self, 'instance') and self.instance.pk:
            self.previous_student_id = self.instance.student_id

    def save(self, commit=False):
        instance = super(CardForm, self).save(commit=False)
        if self.previous_student_id != instance.student_id:
            instance.update_cache_student()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = ('id', 'student', 'i_rarity', 'i_weapon', 'name', 'japanese_name', 'image', 'art', 'transparent',
                  'subcard_effect', 'card_type', 'hp_1', 'sp_1', 'atk_1', 'def_1', 'hp_50', 'sp_50', 'atk_50', 'def_50',
                  'hp_70', 'sp_70', 'atk_70', 'def_70', 'skill_name', 'japanese_skill_name', 'skill_SP',
                  'skill_range', 'skill_comment', 'skill_preview', 'action_skill_damage',
                  'action_skill_combo', 'action_skill_effects', 'evolved_action_skill_damage',
                  'evolved_action_skill_combo', 'evolved_action_skill_effects', 'nakayoshi_title',
                  'japanese_nakayoshi_title', 'nakayoshi_skill_effect', 'nakayoshi_skill_target',
                  'evolved_nakayoshi_skill_effect', 'evolved_nakayoshi_skill_target', 'charge_name', 'charge_hit',
                  'charge_damage', 'charge_range', 'charge_comment',)
        optional_fields = (
            'name', 'japanese_name', 'art', 'transparent', 'subcard_effect', 'card_type', 'hp_1', 'sp_1', 'atk_1',
            'def_1', 'hp_50', 'sp_50', 'atk_50', 'def_50', 'hp_70', 'sp_70', 'atk_70', 'def_70', 'skill_name',
            'japanese_skill_name', 'skill_SP', 'skill_range', 'skill_comment', 'skill_preview',
            'action_skill_damage', 'action_skill_combo', 'action_skill_effects',
            'evolved_action_skill_damage', 'evolved_action_skill_combo', 'evolved_action_skill_effects',
            'nakayoshi_title', 'japanese_nakayoshi_title', 'nakayoshi_skill_effect', 'nakayoshi_skill_target',
            'evolved_nakayoshi_skill_effect', 'evolved_nakayoshi_skill_target', 'charge_name', 'charge_hit',
            'charge_damage', 'charge_range', 'charge_comment',)


class CardFilterForm(MagiFiltersForm):
    search_fields = ['_cache_student_name', '_cache_student_japanese_name', 'name', 'japanese_name', 'skill_name',
                     'japanese_skill_name']
    ordering_fields = [
        ('id', _('ID')),
        ('_cache_student_name', string_concat(_('Student'), ' - ', _('Name'))),
        ('_cache_student_japanese_name', string_concat(_('Student'), ' - ', _('Name'), ' (', t['Japanese'], ')')),
        ('i_rarity', _('Rarity')),
        ('i_weapon', _('Weapon')),
        ('hp_1', string_concat(_('HP'), ' (', _('Level 1'), ')')),
        ('sp_1', string_concat(_('SP'), ' (', _('Level 1'), ')')),
        ('atk_1', string_concat(_('ATK'), ' (', _('Level 1'), ')')),
        ('def_1', string_concat(_('DEF'), ' (', _('Level 1'), ')')),
        ('hp_50', string_concat(_('HP'), ' (', _('Level 50'), ')')),
        ('sp_50', string_concat(_('SP'), ' (', _('Level 50'), ')')),
        ('atk_50', string_concat(_('ATK'), ' (', _('Level 50'), ')')),
        ('def_50', string_concat(_('DEF'), ' (', _('Level 50'), ')')),
    ]

    def _evolvable_to_queryset(form, queryset, request, value):
        if value == '2':
            return queryset.filter(i_rarity__in=EVOLVABLE_RARITIES, card_type=0)
        elif value == '3':
            return queryset.exclude(i_rarity__in=EVOLVABLE_RARITIES, card_type=0)
        return queryset

    evolvable = forms.NullBooleanField(initial=None, required=False, label=_('Evolvable'))
    evolvable_filter = MagiFilter(to_queryset=_evolvable_to_queryset)

    card_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + CARDTYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CardFilterForm, self).__init__(*args, **kwargs)
        self.fields['reverse_order'].initial = False

    class Meta:
        model = models.Card
        fields = ('search', 'student', 'card_type', 'i_rarity', 'i_weapon', 'evolvable', 'ordering', 'reverse_order')


############################################################
# Owned Card

class OwnedCardFilterForm(MagiFiltersForm):
    search_fields = CardFilterForm.search_fields

    class Meta:
        model = models.Card
        fields = ('search', 'i_rarity', 'i_weapon')
        optional_fields = ('i_rarity')

class OwnedCardEditForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(OwnedCardEditForm, self).__init__(*args, **kwargs)
        self.card = self.instance.card

    def save(self, commit=False):
        instance = super(OwnedCardEditForm, self).save(commit=False)
        if self.card.i_rarity == models.RARITY_N and instance.level > 50:
            instance.star_rank = 50
        if commit:
            instance.save()
        return instance

    def clean_obtained_date(self):
        if 'obtained_date' in self.cleaned_data:
            if self.cleaned_data['obtained_date']:
                if self.cleaned_data['obtained_date'] < datetime.date(2015, 4, 16):
                    raise forms.ValidationError(_('The game didn\'t even exist at that time.'))
                if self.cleaned_data['obtained_date'] > datetime.date.today():
                    raise forms.ValidationError(_('This date cannot be in the future.'))
        return self.cleaned_data['obtained_date']

    class Meta:
        model = models.OwnedCard
        fields = ('evolved', 'level', 'obtained_date')
        optional_fields = ('evolved', 'level', 'obtained_date')
        date_fields = ('obtained_date',)

############################################################
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
        ('episode', _('ID')),
        ('easy_stage__level', _('Easy Level')),
        ('easy_stage__exp', _('Easy EXP')),
        ('easy_stage__coins', _('Easy Coins')),
        ('easy_stage__cheerpoint', _('Easy Cheerpoints')),
        ('normal_stage__level', _('Normal Level')),
        ('normal_stage__exp', _('Normal EXP')),
        ('normal_stage__coins', _('Normal Coins')),
        ('normal_stage__cheerpoint', _('Normal Cheerpoints')),
        ('hard_stage__level', _('Hard Level')),
        ('hard_stage__exp', _('Hard EXP')),
        ('hard_stage__coins', _('Hard Coins')),
        ('hard_stage__cheerpoint', _('Hard Cheerpoints')),
    ]


    def __init__(self, *args, **kwargs):
        super(StageFilterForm, self).__init__(*args, **kwargs)
        self.fields['reverse_order'].initial = False

    class Meta:
        model = models.Stage
        fields = ('search', 'part')


############################################################
# Irous Variation

class IrousVariationFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    is_large_irous = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(enumerate([True, False])))

    class Meta:
        model = models.IrousVariation
        fields = ('search', 'species', "is_large_irous")
