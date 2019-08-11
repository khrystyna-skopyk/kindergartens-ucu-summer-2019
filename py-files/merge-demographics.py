import csv
from collections import defaultdict
import re
import json

abbrevs_to_remove = ('пров.', 'просп.', 'пл.', 'вул.')
manual_map = {'Айвазовського І ':'Айвазовського І.',
'Богомольця О   акад ':'Богомольця О., акад.',
'Бортнянського Д ':'Бортнянського Д.',
'Буйка П.. проф.':'Буйка П., проф.',
'Величковського І ':'Величковського І.',
'Виговського І ':'Виговського І.',
'Грінченка Б ':'Грінченка Б.',
'Гірника О ':'Гірника О.',
'Дороша Ю ':'Дороша Ю.',
'Дорошенка П ':'Дорошенка П.',
'Здоров’я':"Здоров'я",
'Кам’янецька':"Кам'янецька",
'Квітки-Основ’яненка Г.':"Квітки-Основ'яненка Г.",
'Коновальця Є ':'Коновальця Є.',
'Коперника М ':'Коперника М.',
'Котляревського І ':'Котляревського І.',
'Крип’якевича І.. акад.':"Крип'якевича І., акад.",
'Кубійовича В ': 'Кубійовича В.',
'Ластів’яча': "Ластів'яча",
'Левицького К ':'Левицького К.',
'Лижв’ярська': "Лижв'ярська",
'Липинського В ': 'Липинського В.',
'Лінкольна А ':'Лінкольна А.',
'Мазепи І   гетьм ':'Мазепи І., гетьм.',
'Миколайчука І ':'Миколайчука І.',
'Над’ярна':"Над'ярна",
'П’ясецького А.':"П'ясецького А.",
'Ринок  пл ':'Ринок, пл.',
'Сахарова А  акад ':'Сахарова А.,акад.',
'Свободи  просп ':'Свободи, просп.',
'Солов’їна':"Солов'їна",
'Солом’янка': "Солом'янка",
'Стефаника В ':'Стефаника В.',
'Торф’яна': "Торф'яна",
'Турянського О ':'Турянського О.',
'Фредра О ':'Фредра О.',
'Хвильового М ':'Хвильового М.',
'Червоної Калини  просп.': 'Червоної Калини, просп.',
'Чорновола В  просп ':'Чорновола В.,просп.',
'Чупринки Т  ген ': 'Чупринки Т.,ген.',
'Чучмана І.': 'Чучмана Ю.',
'Шевченка Т ': 'Шевченка Т.',
'Шевченка Т. ': 'Шевченка Т.'}


def compare_two_files(coords_file, population_file):
    """
    !!!
    :param coords_file: a file with street names and their geolocation
    :param population_file: a file with street names and the number of people living there
    :return: None
    """
    demog_set = set()
    coord_set = set()
    coord_csvfile = open(coords_file)
    coord_readCSV = csv.reader(coord_csvfile, delimiter=',')
    for row in coord_readCSV:
        coord_set.add(row[4])
    with open(population_file, encoding='cp1251') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        # header = readCSV.next()
        for row in readCSV:
            str_name = row[0]
            if row[0].startswith(abbrevs_to_remove):
                str_name = row[0][row[0].find(".") + 1:]
            if str_name in manual_map:
                str_name = manual_map[str_name]
            demog_set.add(str_name)
    print(len(demog_set))
    d_diff = demog_set.difference(coord_set)
    print(len(d_diff))
    print(sorted(d_diff))
    print(len(coord_set))
    c_diff = coord_set.difference(demog_set)
    print(len(c_diff))
    print(sorted(c_diff))


if __name__ == "__main__":
    compare_two_files('data/adresses_and_coord.csv', 'data/demography.csv')