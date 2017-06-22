import csv

from hoshimori.models import *


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
                    owner_id=1,
                )


character_import_data()


def irousu_species_import_data():
    with open('database\irousu_species.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'name':  # ignore header row
                id += 1
                _, created = Irousu.objects.get_or_create(
                    id=id,
                    name=row[0],
                    weak=row[1],
                    strong=row[2],
                    guard=row[3],
                )


irousu_species_import_data()


def irousu_import_data():
    with open('database\irousu.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'species':  # ignore header row
                id += 1
                _, created = IrousuVariation.objects.get_or_create(
                    id=id,
                    species_id=row[0],
                    japanese_name=row[1],
                    name=row[2],
                    image=row[3],
                )


irousu_import_data()


def stage_import_data():
    with open('database\stage_database.csv') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            if row[0] != 'stage_name':  # ignore header row
                id += 1
                # Add stage
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
                    stage_id=id,
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
                    stage_id=id,
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
                    stage_id=id,
                    difficulty=HARD,
                    level=row[14],
                    exp=row[15],
                    coins=row[16],
                    cheerpoints=row[17],
                    objectives=row[18]
                )

                # Add Irousus
                small_irousus = row[19]
                large_irousus = row[20]

                # Split 'em up and add small irousus
                for irousu in small_irousus.split(','):
                    if irousu != "":
                        _, created = Stage.small_irousu.through.objects.get_or_create(
                            stage_id=id,
                            irousuvariation_id=irousu,
                        )

                # Split 'em up and add big irousus
                for irousu in large_irousus.split(','):
                    if irousu != "":
                        _, created = Stage.large_irousu.through.objects.get_or_create(
                            stage_id=id,
                            irousuvariation_id=irousu,
                        )


stage_import_data()


# TODO
def card_import_data():
    with open('C:\Users\kokon\PycharmProjects\hoshimori_scrapy\hoshimori\results\normal_database.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'name':  # ignore header row
                _, created = Card.objects.get_or_create(
                    card_type=row[0],
                    character=row[1],
                    event=row[2],
                    card_name=row[3],
                    card_image=row[4],
                    weapon_type=row[5],
                    weapon_image=row[6],
                    rarity=row[7],
                    stat1_hp=row[8],
                    stat1_sp=row[9],
                    stat1_atk=row[10],
                    stat1_def=row[11],
                    stat50_hp=row[12],
                    stat50_sp=row[13],
                    stat50_atk=row[14],
                    stat50_def=row[15],
                    stat70_hp=row[16],
                    stat70_sp=row[17],
                    stat70_atk=row[18],
                    stat70_def=row[19],
                    skill_name=row[20],
                    skill_sp=row[21],
                    skill_combo=row[22],
                    skill_hit=row[23],
                    skill_damage=row[24],
                    skill_range=row[25],
                    skill_effect=row[26],
                    skill_comment=row[27],
                    skill_preview=row[28],
                    charge_name=row[29],
                    charge_hit=row[30],
                    charge_damage=row[31],
                    charge_range=row[32],
                    charge_comment=row[33],
                    nakayoshi_title=row[34],
                    # japanese_nakayoshi_title=row[34],
                    # nakayoshi_target_noevol=row[35],
                    # nakayoshi_effect_noevol=row[36],
                    # nakayoshi_target_evol=row[37],
                    # nakayoshi_effect_evol=row[38],
                )


card_import_data()
