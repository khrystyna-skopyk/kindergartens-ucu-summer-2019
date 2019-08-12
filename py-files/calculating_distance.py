import pandas as pd 

#In this file I calculate distances and then I do some dataframe edits to make the files workable. 
from math import sin, cos, sqrt, atan2, radians

zdo = pd.read_csv('zdo_cleaned.csv')


order_data = pd.read_csv('add_distances.csv')


def distance(lat1, lon1):
    #   approximate radius of earth in km
    R = 6373.0
    distances = []
    lat1 = radians(lat1)
    lon1 = radians(lon1)

    for i in range(len(zdo)):
        lat2 = radians(zdo.iloc[i]['latitude'])
        lon2 = radians(zdo.iloc[i]['longitude'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        distances.append(distance)
    
    return min(distances), distances.index(min(distances))

order_data


p = []

for k in range(len(order_data)):
    p.append(distance(order_data.iloc[k]['Y'], order_data.iloc[k]['X']))
p

distance(order_data.iloc[5]['latitude'], order_data.iloc[5]['longitude'])
order_data.drop(order_data[order_data['class'] == 'kindergarden'].index, inplace = True)

order_data['distance/zdo'] = p

order_data


j = p[5:]

order_data
order_data['distance/zdo'] = j

order_data.to_csv('order_data_with_distances_1.csv')

distances
distances = order_data
distances.columns = ['index', 'index.1', 'UNIQ', 'CREATE', 'ENTER', 'ZDO1', 'ZDO2', 'ZDO3',
       'GROUP', 'BENEFITS', 'CITY', 'STREET', 'HOUSE', 'HOUSESYMBOL',
       'APPARTMENT', 'MAINCITY', 'SCODE', 'X', 'Y', 'address', 'distance/zdo']

distances = pd.read_csv('order_data_with_distances_1.csv')



distances['distance/zdo'] = distances['distance/zdo'].apply(lambda x: str(x).replace('(', ''))
distances['distance/zdo'] = distances['distance/zdo'].apply(lambda x: str(x).replace(')', ''))

distances[['distance', 'zdo']] = distances['distance/zdo'].str.split(',', 1, expand=True)
distances.drop(['distance/zdo'], axis = 1, inplace = True)

distances


# add geo info for kindergardens
distances['latitude_for_kindergarden'] = 0
distances['longitude_for_kindergarden'] = 0

distances['zdo'] = pd.to_numeric(distances['zdo'])
distances['latitude_for_kindergarden'] = distances['zdo'].apply(lambda x: zdo.loc[zdo['Unnamed: 0'] == x, 'latitude'].values)
distances['longitude_for_kindergarden'] = distances['zdo'].apply(lambda x: zdo.loc[zdo['Unnamed: 0'] == x, 'longitude'].values)

distances.to_csv('distances_full2.csv')
distances

distances['latitude_for_kindergarden'] = distances['latitude_for_kindergarden'].apply(lambda x: float(x))
distances['longitude_for_kindergarden'] = distances['longitude_for_kindergarden'].apply(lambda x: float(x))

distances_simple = distances[['latitude', 'longitude', 'latitude_for_kindergarden', 'longitude_for_kindergarden']]

distances['CITY'].unique()

distances.columns

distances['distance'] = pd.to_numeric(distances['distance'])
distances['distance'].loc[distances['distance'] >= 0.4].count()/len(distances)

distances['MAINCITY'].sum
        