import csv
import re

from hoshimori.models import *


###########################################################
# Student

def character_import_data():
    with open('database\characters.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'name':  # ignore header row
                id += 1
                _, created = Student.objects.get_or_create(
                    id=id,
                    name=row[0],
                    japanese_name=row[1],
                    unlock=row[2],
                    description=row[3],
                    i_school_year=row[4],
                    birthday=row[5],
                    i_star_sign=row[6],
                    i_blood_type=row[7],
                    extra_activity=row[8],
                    catchphrase_1=row[9],
                    catchphrase_2=row[10],
                    height=row[11],
                    weight=row[12],
                    bust=row[13],
                    waist=row[14],
                    hip=row[15],
                    hobby_1=row[16],
                    hobby_2=row[17],
                    hobby_3=row[18],
                    food_likes=row[19],
                    food_dislikes=row[20],
                    family=row[21],
                    dream=row[22],
                    ideal_1=row[23],
                    ideal_2=row[24],
                    ideal_3=row[25],
                    pastime=row[26],
                    destress=row[27],
                    fav_memory=row[28],
                    fav_phrase=row[29],
                    secret=row[30],
                    CV=row[31],
                    romaji_CV=row[32],
                    image=row[33],
                    full_image=row[34],
                    signature=row[35],
                    phrase_1=row[36],
                    phrase_2=row[37],
                    introduction_1=row[38],
                    introduction_2=row[39],
                    owner_id=1,
                )


character_import_data()


###########################################################
# Irous

def irous_species_import_data():
    with open('database\irous_species.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'name':  # ignore header row
                id += 1
                _, created = Irous.objects.get_or_create(
                    id=id,
                    name=row[0],
                    weak=row[1],
                    strong=row[2],
                    guard=row[3],
                )


irous_species_import_data()


def irous_import_data():
    with open('database\irous.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'species':  # ignore header row
                id += 1
                _, created = IrousVariation.objects.get_or_create(
                    id=id,
                    species_id=row[0],
                    japanese_name=row[1],
                    name=row[2],
                    image=row[3],
                    is_large_irous=True if row[4] == "1" else False,
                )


irous_import_data()


###########################################################
# Stage

def stage_import_data():
    with open('database\stage_database.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'stage_name':  # ignore header row
                id += 1
                # Add stage if not added
                if Stage.objects.filter(name=row[0]).__len__() == 0:
                    _, created = Stage.objects.get_or_create(
                        id=id,
                        owner_id=1,
                        name=row[0],
                        part=row[1],
                        episode=row[2],
                        number=row[3],
                        materials=row[21],
                        easy_stage_id=id * 3 - 2,
                        normal_stage_id=id * 3 - 1,
                        hard_stage_id=id * 3,
                    )

                    # Add difficulty
                    # Easy
                    _, created = StageDifficulty.objects.get_or_create(
                        id=id * 3 - 2,
                        difficulty=EASY,
                        level=row[4],
                        exp=row[5],
                        coins=row[6],
                        cheerpoints=row[7],
                        objectives=row[8],
                    )
                    # Normal
                    _, created = StageDifficulty.objects.get_or_create(
                        id=id * 3 - 1,
                        difficulty=NORMAL,
                        level=row[9],
                        exp=row[10],
                        coins=row[11],
                        cheerpoints=row[12],
                        objectives=row[13]
                    )
                    # Hard
                    _, created = StageDifficulty.objects.get_or_create(
                        id=id * 3,
                        difficulty=HARD,
                        level=row[14],
                        exp=row[15],
                        coins=row[16],
                        cheerpoints=row[17],
                        objectives=row[18]
                    )

                    # Add Irouss
                    small_irous = row[19]
                    large_irous = row[20]

                    # Split 'em up and add small irouss
                    for irous in small_irous.split(','):
                        if irous != "":
                            _, created = Stage.small_irous.through.objects.get_or_create(
                                stage_id=id,
                                irousvariation_id=irous,
                            )

                    # Split 'em up and add big irouss
                    for irous in large_irous.split(','):
                        if irous != "":
                            _, created = Stage.large_irous.through.objects.get_or_create(
                                stage_id=id,
                                irousvariation_id=irous,
                            )


stage_import_data()


###########################################################
# Card

def extract_number(str):
    return re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", str)


def return_number_or_none(str):
    if str.isdigit():
        return str
    else:
        return None


# TODO
def card_import_data():
    with open('database\card_database.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            try:
                if row[0] != 'card_type':  # ignore header row
                    id += 1
                    if Card.objects.filter(name=row[3]).__len__() == 0:
                        _, created = Card.objects.get_or_create(
                            id=id,
                            i_rarity=row[7],
                            i_weapon=row[5],
                            name=row[3],
                            japanese_name=row[3],
                            image=row[4],
                            art=row[4],
                            transparent=row[4],
                            subcard_effect=0,
                            card_type=row[0],
                            hp_1=row[8],
                            sp_1=row[9],
                            atk_1=row[10],
                            def_1=row[11],
                            hp_50=row[12],
                            sp_50=row[13],
                            atk_50=row[14],
                            def_50=row[15],
                            hp_70=return_number_or_none(row[16]),
                            sp_70=return_number_or_none(row[17]),
                            atk_70=return_number_or_none(row[18]),
                            def_70=return_number_or_none(row[19]),
                            skill_name=row[20],
                            japanese_skill_name=row[20],
                            skill_SP=return_number_or_none(row[21]),
                            skill_hits=return_number_or_none(row[23]),
                            skill_range=row[25],
                            skill_comment=row[27],
                            skill_preview=row[28],
                            max_damage=0,
                            action_skill_damage=row[24],
                            action_skill_combo=row[22] if row[22].isdigit() else None if row[22] == "" else
                            extract_number(row[22])[0],
                            action_skill_effects=row[26],
                            evolved_action_skill_damage=row[24],
                            evolved_action_skill_combo=row[22] if row[22].isdigit() else None if row[22] == "" else
                            extract_number(row[22])[1],
                            evolved_action_skill_effects=row[26],
                            nakayoshi_title=row[34],
                            japanese_nakayoshi_title=row[34],
                            nakayoshi_skill_effect=row[36],
                            nakayoshi_skill_target=row[35],
                            evolved_nakayoshi_skill_effect=row[38],
                            evolved_nakayoshi_skill_target=row[37],
                            charge_name=row[29],
                            charge_hit=None if row[30] == '' else row[30],
                            charge_damage=row[31],
                            charge_range=row[32],
                            charge_comment=row[33],
                            owner_id=1,
                            student_id=return_number_or_none(row[1]),
                        )
            except Exception, e:
                print str(e)
                print id
                print row[3]
                break


card_import_data()
