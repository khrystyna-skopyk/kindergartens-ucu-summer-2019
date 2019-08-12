# in thie file I create a grid map of the city of Lviv.

import pandas as pd 
import numpy as np 

distances_data = pd.read_csv('distances_full.csv')

lat = list(np.arange(49.75, 49.93, 1/500).round(5))


lon = list(np.arange(23.91, 24.1, 1/500).round(5))


grids = []
for k in range(1,len(lon)):
    for j in range(1, len(lat)):
        grids.append([[lat[j-1], lat[j]], [lon[k-1], lon[k]]])




order_data_grids = []
for i in range(len(distances_data)):
    data = distances_data.iloc[i]
    latitude = data['Y']
    longitude = data['X']

    list_lat = []
    list_lon = []

    for k in range(0, len(lat)):
        if (lat[k] - latitude) >= 0:
            lat_k = lat[k].round(5)
            break
    for j in range(0, len(lon)):
        if (lon[j] - longitude) >= 0:
            lon_j = lon[j].round(5)
            break
    order_data_grids.append([lat_k, lon_j])



order_data_grids1 = pd.DataFrame(order_data_grids)



order_data_grids1['lat'] = order_data_grids1[0].apply(lambda x: lat.index(x))
order_data_grids1['lon'] =order_data_grids1[1].apply(lambda x: lon.index(x))


distance = pd.read_csv('for_nastia_graphs.csv')



#### Add the distance to the nearest one. 

zeros_count = np.zeros(len(lat) * len(lon))
zeros_function = np.zeros(len(lat) * len(lon))
order_data_grids1
for i in range(len(order_data_grids1)):
    index = len(lat)*order_data_grids1['lon'][i] + order_data_grids1['lat'][i]
    if distances_data['distance'][i] <= 400:
        zeros_function[index] += distances_data['distance'][i]
        zeros_count[index] += 1



c = np.divide(zeros_function, zeros_count, out=np.zeros_like(zeros_function), where=zeros_count!=0)


MATRIX = np.reshape(zeros_function, (len(lat), len(lon)), order = 'F')

import matplotlib.pyplot as plt 
import seaborn as sns


MATRIX = np.flip(MATRIX, 0)
plt.figure(figsize = [3,3])
plt.imshow(MATRIX)
plt.show()
plt.savefig('for_presentation1')


distances['latitude_for_kindergarden'] = distances['latitude_for_kindergarden'].apply(lambda x: float(x))
distances['longitude_for_kindergarden'] = distances['longitude_for_kindergarden'].apply(lambda x: float(x))
distances.to_csv('beauty_data.csv')




