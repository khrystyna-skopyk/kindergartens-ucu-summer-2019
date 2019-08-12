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
    Compares the names of the streets from two different files. The results were used to standardize the street names
    ==> ___
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


def standardize_street_names(population_file):
    """
    Using the tips from compare_two_files, standardizes the street names in one file.
    :param population_file: a file with street names and the number of people living there
    :return: None, creates a new file with updated street names
    """
    with open(population_file, encoding='cp1251') as demog_csv:
        with open(population_file, 'w') as demog_new_csv:
            reader = csv.reader(demog_csv, delimiter=';')
            header = next(reader, None)

            writer = csv.writer(demog_new_csv, delimiter=';')
            writer.writerow(header)

            for row in reader:
                str_name = row[0]
                if row[0].startswith(abbrevs_to_remove):
                    str_name = row[0][row[0].find(".") + 1:]
                if str_name in manual_map:
                    str_name = manual_map[str_name]
                row_upd = [str_name] + row[1:]
                writer.writerow(row_upd)


def merge_popul_and_geoloc(coords_file, population_file, resulting_file):
    """
    Merges the two files into one, saving only several necessary datapoint.
    :param coords_file: a file with street names and their geolocation
    :param population_file: a file with street names and the number of people living there
    :param resulting_file: a file with merged data, json format
    :return: None, creates a new file with geolocation and population
    """
    demography_dict = defaultdict(lambda: defaultdict(dict))

    with open(population_file) as demog_csv:
        reader = csv.reader(demog_csv, delimiter=';')
        next(reader, None)
        for row in reader:
            street = row[0]
            housenumber = re.sub(r'[а-я]+', '', row[1])
            n_of_ppl = int(row[-1].replace(" ", ""))
            if demography_dict[street][housenumber].get("ppl"):
                demography_dict[street][housenumber]["ppl"] += n_of_ppl
            else:
                demography_dict[street][housenumber]["ppl"] = n_of_ppl

    with open(coords_file) as coords_csv:
        reader = csv.reader(coords_csv, delimiter=',')
        next(reader, None)
        for row in reader:
            latitude = row[-1]
            longitude = row[-2]
            housenumber = re.sub(r'[а-я]+', '', row[2])
            street = row[4]
            if demography_dict.get(street):
                if demography_dict[street].get(housenumber):
                    demography_dict[street][housenumber]["lat"] = latitude
                    demography_dict[street][housenumber]["long"] = longitude

    with open(resulting_file, 'w') as outfile:
        json.dump(demography_dict, outfile)


def create_kepler_file(input_density_f, output_density_f):
    """
    From json-file, creates kepler-friendly csv file to vizualize the population density in Lviv.
    :param input_density_f: input file with json data on density
    :param output_density_f: output csv file on density
    :return: None, creates a new file
    """
    with open(input_density_f) as json_file:
        with open(output_density_f, 'w') as demog_new_csv:
            data = json.load(json_file)
            writer = csv.writer(demog_new_csv, delimiter=',')
            writer.writerow(['lat', 'long', 'number_of_people'])
            for street in data:
                for hnumber in data[street]:
                    if data[street][hnumber].get("lat"):
                        writer.writerow([data[street][hnumber]["lat"],
                                         data[street][hnumber]["long"],
                                         data[street][hnumber]["ppl"]])


if __name__ == "__main__":
    # compare_two_files('data/adresses_and_coord.csv', 'data/demography.csv')
    # standardize_street_names('data/demography.csv')
    # merge_popul_and_geoloc('data/adresses_and_coord.csv', 'data/demography_upd.csv', 'data/demog_w_coord.txt')
    create_kepler_file('data/demog_w_coord.txt', 'data/density.csv')