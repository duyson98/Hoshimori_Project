# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

############################################################
# Members

ENGLISH_STAR_SIGNS = [
    'Leo',
    'Aries',
    'Libra',
    'Virgo',
    'Scorpio',
    'Capricorn',
    'Pisces',
    'Gemini',
    'Cancer',
    'Sagittarius',
    'Aquarius',
    'Taurus',
]
ENGLISH_STAR_SIGN_CHOICES = list(enumerate(ENGLISH_STAR_SIGNS))
ENGLISH_STAR_SIGN_DICT = dict(ENGLISH_STAR_SIGN_CHOICES)
STAR_SIGN_REVERSE_DICT = {value: key for (key, value) in list(enumerate(ENGLISH_STAR_SIGNS))}
STAR_SIGNS = [
    _('Leo'),
    _('Aries'),
    _('Libra'),
    _('Virgo'),
    _('Scorpio'),
    _('Capricorn'),
    _('Pisces'),
    _('Gemini'),
    _('Cancer'),
    _('Sagittarius'),
    _('Aquarius'),
    _('Taurus'),
]
STAR_SIGN_CHOICES = list(enumerate(STAR_SIGNS))
STAR_SIGN_DICT = dict(STAR_SIGN_CHOICES)

SCHOOL_YEARS = [
    _('Middle School Year 1'),
    _('Middle School Year 2'),
    _('Middle School Year 3'),
    _('High School Year 1'),
    _('High School Year 2'),
    _('High School Year 3'),
]

ENGLISH_SCHOOL_YEARS = [
    'Middle School Year 1',
    'Middle School Year 2',
    'Middle School Year 3',
    'High School Year 1',
    'High School Year 2',
    'High School Year 3',
]

SCHOOL_YEAR_CHOICES = list(enumerate(SCHOOL_YEARS))
SCHOOL_YEAR_DICT = dict(SCHOOL_YEAR_CHOICES)

ENGLISH_SCHOOL_YEAR_CHOICES = list(enumerate(ENGLISH_SCHOOL_YEARS))
ENGLISH_SCHOOL_YEAR_DICT = dict(ENGLISH_SCHOOL_YEAR_CHOICES)

BLOOD_TYPES = ['O', 'A', 'B', 'AB']
BLOOD_TYPE_CHOICES = list(enumerate(BLOOD_TYPES))
BLOOD_TYPE_DICT = dict(BLOOD_TYPE_CHOICES)
BLOOD_TYPE_REVERSE_DICT = {value: key for (key, value) in BLOOD_TYPE_CHOICES}

############################################################
# Accounts

OS = ['iOs', 'Android']
OS_CHOICES = list(enumerate(OS))
OS_DICT = dict(OS_CHOICES)

PLAYERTYPE = ['Free-to-play', 'Pay-to-win', 'FTP PTW Hybrid']
PLAYERTYPE_CHOICES = list(enumerate(PLAYERTYPE))
PLAYERTYPE_DICT = dict(PLAYERTYPE_CHOICES)

############################################################
# Cards

# Card types
NORMAL_CARD = 0
EXTRA_CARD = 1
SUB_CARD = 2

CARDTYPE_CHOICES = [
    (NORMAL_CARD, _('Normal')),
    (EXTRA_CARD, _('Extra')),
    (SUB_CARD, _('Subcard')),
]

CARDTYPE_DICT = dict(CARDTYPE_CHOICES)

# Rarities

RARITY_N = 0
RARITY_R = 1
RARITY_SR = 2
RARITY_SSR = 3
RARITY_UR = 4

RARITY_CHOICES = [
    (RARITY_N, u'★'),
    (RARITY_R, u'★★'),
    (RARITY_SR, u'★★★'),
    (RARITY_SSR, u'★★★★'),
    (RARITY_UR, u'★★★★★'),
]
RARITY_DICT = dict(RARITY_CHOICES)

EVOLVABLE_RARITIES = [RARITY_SR, RARITY_SSR]

# Extrapolated values

EVOLVED_BONUS_PARAMETER_INTERCEPT_3_50 = [
    ('hp', 33.84615385),
    ('sp', 7.923076923),
    ('atk', 13.92307692),
    ('def', 13.92307692),
]
EVOLVED_BONUS_PARAMETER_INTERCEPT_3_70 = [
    ('hp', -20.0),
    ('sp', -4.0),
    ('atk', -8.0),
    ('def', -8.0),
]
EVOLVED_BONUS_PARAMETER_INTERCEPT_4_50 = [
    ('hp', 44.0326087),
    ('sp', 8.812252964),
    ('atk', 17.21047431),
    ('def', 17.36462451),
]
EVOLVED_BONUS_PARAMETER_INTERCEPT_4_70 = [
    ('hp', -25.0),
    ('sp', -5.0),
    ('atk', -10.0),
    ('def', -10.0),
]

EVOLVED_BONUS_PARAMETER_INTERCEPT_4_70_DICT = dict(EVOLVED_BONUS_PARAMETER_INTERCEPT_4_70)
EVOLVED_BONUS_PARAMETER_INTERCEPT_3_50_DICT = dict(EVOLVED_BONUS_PARAMETER_INTERCEPT_3_50)
EVOLVED_BONUS_PARAMETER_INTERCEPT_3_70_DICT = dict(EVOLVED_BONUS_PARAMETER_INTERCEPT_3_70)
EVOLVED_BONUS_PARAMETER_INTERCEPT_4_50_DICT = dict(EVOLVED_BONUS_PARAMETER_INTERCEPT_4_50)

EVOLVED_BONUS_PARAMETER_SLOPE_3_50 = [
    ('hp', 4.923076923),
    ('sp', 0.961538462),
    ('atk', 1.961538462),
    ('def', 1.961538462),
]
EVOLVED_BONUS_PARAMETER_SLOPE_3_70 = [
    ('hp', 6.0),
    ('sp', 1.2),
    ('atk', 2.4),
    ('def', 2.4),
]
EVOLVED_BONUS_PARAMETER_SLOPE_4_50 = [
    ('hp', 6.119565217),
    ('sp', 1.223320158),
    ('atk', 2.459486166),
    ('def', 2.455533597),
]
EVOLVED_BONUS_PARAMETER_SLOPE_4_70 = [
    ('hp', 7.5),
    ('sp', 1.5),
    ('atk', 3.0),
    ('def', 3.0),
]

EVOLVED_BONUS_PARAMETER_SLOPE_4_70_DICT = dict(EVOLVED_BONUS_PARAMETER_SLOPE_4_70)
EVOLVED_BONUS_PARAMETER_SLOPE_3_50_DICT = dict(EVOLVED_BONUS_PARAMETER_SLOPE_3_50)
EVOLVED_BONUS_PARAMETER_SLOPE_3_70_DICT = dict(EVOLVED_BONUS_PARAMETER_SLOPE_3_70)
EVOLVED_BONUS_PARAMETER_SLOPE_4_50_DICT = dict(EVOLVED_BONUS_PARAMETER_SLOPE_4_50)

EXP_TO_NEXT_LEVEL = [
    5, 25, 52, 86, 126, 170, 218, 270, 326, 385, 448, 512, 582, 652, 726, 802, 882, 962, 1046, 1133, 1220, 1311, 1403,
    1498, 1594, 1694, 1793, 1896, 2001, 2106, 2215, 2324, 2437, 2549, 2664, 2781, 2899, 3020, 3141, 3264, 3388, 3515,
    3643, 3772, 3903, 4035, 4169, 4305, 4440, 4579, 4719, 4859, 5001, 5145, 5290, 5436, 5584, 5732, 5883, 6034, 6187,
    6341, 6497, 6653, 6810, 6970, 7130, 7291, 7454
]

ACCUMULATIVE_EXP = [
    5, 30, 82, 168, 294, 464, 682, 952, 1278, 1663, 2111, 2623, 3205, 3857, 4583, 5385, 6267, 7229, 8275, 9408, 10628,
    11939, 13342, 14840, 16434, 18128, 19921, 21817, 23818, 25924, 28139, 30463, 32900, 35449, 38113, 40894, 43793,
    46813, 49954, 53218, 56606, 60121, 63764, 67536, 71439, 75474, 79643, 83948, 88388, 92967, 97686, 102545, 107546,
    112691, 117981, 123417, 129001, 134733, 140616, 146650, 152837, 159178, 165675, 172328, 179138, 186108, 193238,
    200529, 207983
]

############################################################
# Weapons

WEAPON_SWORD = 0
WEAPON_SPEAR = 1
WEAPON_HAMMER = 2
WEAPON_GUN = 3
WEAPON_ROD = 4
WEAPON_GUNBLADE = 5
WEAPON_TWINBARRETT = 6

WEAPON_CHOICES = [
    (WEAPON_SWORD, _('Sword')),
    (WEAPON_SPEAR, _('Spear')),
    (WEAPON_HAMMER, _('Hammer')),
    (WEAPON_GUN, _('Gun')),
    (WEAPON_ROD, _('Rod')),
    (WEAPON_GUNBLADE, _('Gunblade')),
    (WEAPON_TWINBARRETT, _('Twin Barrett')),
]

WEAPON_DICT = dict(WEAPON_CHOICES)

ENGLISH_WEAPON_CHOICES = [
    (WEAPON_SWORD, 'Sword'),
    (WEAPON_SPEAR, 'Spear'),
    (WEAPON_HAMMER, 'Hammer'),
    (WEAPON_GUN, 'Gun'),
    (WEAPON_ROD, 'Rod'),
    (WEAPON_GUNBLADE, 'Gunblade'),
    (WEAPON_TWINBARRETT, 'Twin Barrett'),
]

ENGLISH_WEAPON_DICT = dict(ENGLISH_WEAPON_CHOICES)

NOT_UPGRADED = 0
ALPHA = 1
BETA = 2
GAMMA = 3

UPGRADE_LEVEL_CHOICES = [
    (NOT_UPGRADED, ''),
    (ALPHA, _('Alpha')),
    (BETA, _('Beta')),
    (GAMMA, _('Gamma')),
]

UPGRADE_LEVEL_DICT = dict(UPGRADE_LEVEL_CHOICES)

############################################################
# Nakayoshi

SKILL_ATK = 0
SKILL_HP = 1
SKILL_SP = 2
SKILL_DAMAGE = 3
SKILL_COMBO_DAMAGE = 4
SKILL_SP_CONSUMPTION = 5
SKILL_SKILL_COMBO = 6
SKILL_MOVEMENT_RATE = 7
SKILL_DODGE = 8
SKILL_AUTO_RELOAD = 9
SKILL_BULLET = 10
SKILL_ITEM_RANGE = 11
SKILL_DROP_QUANTITY = 12
SKILL_COIN = 13
SKILL_CHEERPOINT = 14
SKILL_EXP = 15
SKILL_BOND_POINT = 16
SKILL_GUARD_PENETRATION = 17
SKILL_RECEIVED_DAMAGE = 18
SKILL_NULL_SP = 19
SKILL_NULL_SLOW = 20
SKILL_NULL_PARALYSIS = 21
SKILL_NULL_SKILL_SEAL = 22
SKILL_NULL_POISON = 23

ENGLISH_NAKAYOSHI_SKILLS_CHOICES = [
    (SKILL_ATK, 'ATK'),
    (SKILL_HP, 'HP'),
    (SKILL_SP, 'SP'),
    (SKILL_DAMAGE, 'Damage'),
    (SKILL_COMBO_DAMAGE, 'Combo Damage'),
    (SKILL_SP_CONSUMPTION, 'SP Consumption'),
    (SKILL_SKILL_COMBO, 'Skill Combo'),
    (SKILL_MOVEMENT_RATE, 'Movement Rate'),
    (SKILL_DODGE, 'Dodge'),
    (SKILL_AUTO_RELOAD, 'Auto Reload'),
    (SKILL_BULLET, 'Bullet'),
    (SKILL_ITEM_RANGE, 'Item Recovery Range'),
    (SKILL_DROP_QUANTITY, 'Item Drop Quantity'),
    (SKILL_COIN, 'Coin'),
    (SKILL_CHEERPOINT, 'Cheerpoint'),
    (SKILL_EXP, 'EXP'),
    (SKILL_BOND_POINT, 'Bond Point'),
    (SKILL_GUARD_PENETRATION, 'Guard Penetration'),
    (SKILL_RECEIVED_DAMAGE, 'Received Damage'),
    (SKILL_NULL_SP, 'Null SP Damage'),
    (SKILL_NULL_SLOW, 'Null Slow'),
    (SKILL_NULL_PARALYSIS, 'Null Paralysis'),
    (SKILL_NULL_SKILL_SEAL, 'Null Skill Seal'),
    (SKILL_NULL_POISON, 'Null Poison'),
]

ENGLISH_NAKAYOSHI_SKILLS_DICT = dict(ENGLISH_NAKAYOSHI_SKILLS_CHOICES)

NAKAYOSHI_SKILLS_CHOICES = [
    (SKILL_ATK, _('ATK')),
    (SKILL_HP, _('HP')),
    (SKILL_SP, _('SP')),
    (SKILL_DAMAGE, _('Damage')),
    (SKILL_COMBO_DAMAGE, _('Combo Damage')),
    (SKILL_SP_CONSUMPTION, _('SP Consumption')),
    (SKILL_SKILL_COMBO, _('Skill Combo')),
    (SKILL_MOVEMENT_RATE, _('Movement Rate')),
    (SKILL_DODGE, _('Dodge')),
    (SKILL_AUTO_RELOAD, _('Auto Reload')),
    (SKILL_BULLET, _('Bullet')),
    (SKILL_ITEM_RANGE, _('Item Recovery Range')),
    (SKILL_DROP_QUANTITY, _('Item Drop Quantity')),
    (SKILL_COIN, _('Coin')),
    (SKILL_CHEERPOINT, _('Cheerpoint')),
    (SKILL_EXP, _('EXP')),
    (SKILL_BOND_POINT, _('Bond Point')),
    (SKILL_GUARD_PENETRATION, _('Guard Penetration')),
    (SKILL_RECEIVED_DAMAGE, _('Received Damage')),
    (SKILL_NULL_SP, _('Null SP Damage')),
    (SKILL_NULL_SLOW, _('Null Slow')),
    (SKILL_NULL_PARALYSIS, _('Null Paralysis')),
    (SKILL_NULL_SKILL_SEAL, _('Null Skill Seal')),
    (SKILL_NULL_POISON, _('Null Poison')),
]

NAKAYOSHI_SKILLS_DICT = dict(NAKAYOSHI_SKILLS_CHOICES)

SMALL = 0
MEDIUM = 1
LARGE = 2
SUPER = 3

SKILL_SIZE_CHOICES = [
    (SMALL, _('Small')),
    (MEDIUM, _('Medium')),
    (LARGE, _('Large')),
    (SUPER, _('Super')),
]
SKILL_SIZE_DICT = dict(SKILL_SIZE_CHOICES)

ENGLISH_SKILL_SIZE_CHOICES = [
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
    (SUPER, 'Super'),
]
ENGLISH_SKILL_SIZE_DICT = dict(ENGLISH_SKILL_SIZE_CHOICES)

SKILL_SIZE_VALUE = [
    ("Combo Damage", [10, 15, 20, 30]),
    ("Damage", [6, 8, 10, 15]),
    ("SP Consumption", [5, 10, 15, 25]),
    ("Coin", [50, 100]),
    ("Cheerpoint", [50, 100]),
    ("EXP", [50, 100]),
]
SKILL_SIZE_VALUE_DICT = dict(SKILL_SIZE_VALUE)

############################################################
# Stages

EASY = 0
NORMAL = 1
HARD = 2

DIFFICULTY_CHOICES = [
    (EASY, "Easy"),
    (NORMAL, "Normal"),
    (HARD, "Hard"),
]

DIFFICULTY_DICT = dict(DIFFICULTY_CHOICES)

############################################################
# Irousu

IROUSU_TYPES = [
    'Gel',
    'Rouga',
    'Quinn',
    'Eel',
    'Shum',
    'Draco',
    'Doguu',
    'Spirit',
    'Saiki',
    'Machinery',
    'Valiant',
    'Unknown',
]
IROUSU_TYPE_CHOICES = list(enumerate(IROUSU_TYPES))
IROUSU_TYPE_DICT = dict(IROUSU_TYPE_CHOICES)
