from django.utils.translation import ugettext_lazy as _, string_concat
from web.forms import MagiFiltersForm

from hoshimori import models
from hoshimori.django_translated import t


############################################################
# Student

class StudentFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'birthday', 'description']

    ordering_fields = [
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

class CardFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
    ]

    class Meta:
        model = models.Card
        fields = ('search', 'i_rarity', 'i_weapon', 'card_type')


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

    # ordering_fields = [
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
    # ]

    class Meta:
        model = models.Stage
        fields = ('search', 'part')


############################################################
# Irousu Variation

class IrousuVariationFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']

    class Meta:
        model = models.IrousuVariation
        fields = ('search', 'species')
