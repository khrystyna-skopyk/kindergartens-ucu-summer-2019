import pandas as pd 

# Initial data import

orders_new = pd.read_csv('orders_new.csv', encoding='CP1251', sep = ';')
fact_2018 = pd.read_csv('fact_2018.csv', encoding = 'CP1251', sep = ';')
fact_2019 = pd.read_csv('fact_2019.csv', encoding = 'CP1251', sep = ';')
zdo = pd.read_csv('zdo.csv')
Demographics_2019 = pd.read_csv('Demography_Lviv_2019 (gender,age).csv', encoding = 'CP1251', sep = ';')
Demographics_2019


orders_new = orders_new.apply(lambda x: x.str.replace("'", ""))

l = []
for k in orders_new.columns:
    k = k.replace("'", "")
    l.append(k)

orders_new.columns = l


info =orders_new[['CITY', 'STREET', 'HOUSE']]

info = info.loc[(info['CITY'].str.contains('Львів'))]
info.reset_index(inplace = True)


from geopy.geocoders import Nominatim   

lat = []
lon = []
all_data = []

for i in range(338, len(info)):
    geolocator = Nominatim(timeout=3)

    location = geolocator.geocode(info.iloc[i].values)
    if location == None:
        lat.append(0)
        lon.append(0)
        all_data.append(0)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)
        all_data.append(location)


