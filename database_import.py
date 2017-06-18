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
                )


import_data()
