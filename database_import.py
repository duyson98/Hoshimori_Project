import csv

from hoshimori.models import Student


def import_data():
    with open('C:\Users\kokon\PycharmProjects\hoshimori_scrapy\hoshimori\characters.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'name':  # ignore header row
                _, created = Student.objects.get_or_create(
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


import_data()
