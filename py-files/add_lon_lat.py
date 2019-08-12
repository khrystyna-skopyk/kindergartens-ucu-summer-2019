import pandas as pd 

zdo = pd.read_csv('zdo.csv')
orders_new = pd.read_csv('orders_newest.csv')

orders = pd.read_csv('orders.csv')

# cleaning the data and renaming the columns 
orders_new = orders_new.apply(lambda x: x.str.replace("'", ""))
l = []
for k in orders_new.columns:
    k = k.replace("'", "")
    l.append(k)
orders_new.columns = l

orders_new['MAINCITY'] = pd.to_numeric(orders_new['MAINCITY'])
orders_new['X'] = pd.to_numeric(orders_new['X'])
orders_new['Y'] = pd.to_numeric(orders_new['Y'])

#deleting data not from Lviv
orders_new.drop(orders_new.loc[orders_new['MAINCITY'] == 0].index, inplace = True)
orders_new.reset_index(inplace = True)


info =orders_new[['CITY', 'STREET', 'HOUSE']]
info.reset_index(inplace = True)


orders_new['address'] = info.apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1)

# Deleting data with no city. 
orders_new.drop(orders_new.loc[orders_new['address'] == ',,'].index, inplace = True)

# orders_without is a file that I use to find data points that I need to add geocoding. 
orders_without = orders_new.loc[orders_new['Y'] == 0]
orders_without.reset_index(inplace = True)


### Here I add the geocoded data. 
from geopy import geocoders
geolocator = geocoders.Bing('AhKosYocG5FwWIQP38FMHpfPg8IlrxyTA_QslYIMbbwdUv8qXWKwGppHXTwCSCm_', timeout = 8)

orders_without

lat = []
lon = []
all_data = []


for i in range(709, len(info)):
    df2 = pd.DataFrame([lat,lon,all_data])
    df2.to_csv('lon_lat_for_orders_new_new_new.csv')

    print(i)
    location = geolocator.geocode(orders_without['address'][i], include_country_code='UA')
    if location == None:
        lat.append(0)
        lon.append(0)
        all_data.append(0)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)
        all_data.append(location)


df2 = pd.DataFrame([lat,lon,all_data])
df2 = df2.transpose()

df2.to_csv('lon_lat_for_orders_PLS.csv')


for i in range(len(df2)):
    orders_without.loc[orders_without.index == i, 'X'] = df2[0][i]
    orders_without.loc[orders_without.index == i, 'Y'] = df2[1][i]

orders_new.loc[orders_without['index'], 'X'] = orders_without['X']
orders_new.loc[orders_without['index'], 'Y'] = orders_without['Y']


orders_new.to_csv('venia_added.csv')
###


orders_new = pd.read_csv('lon_lat_full_data.csv')


orders_new.index = orders_new['index']
orders_without
orders_new.index

orders_without.drop(['latitude', 'longitude'], axis = 1, inplace = True)

orders_without['longitude'] = lon
orders_without['latitude'] = lat
orders_without['all_data'] = all_data

info.to_csv('infoOrders.csv')

df5 = pd.read_csv('lon_lat_for_orders.csv')




df5 = df5.transpose() 
df5.columns = df5.iloc[0]
df5

df5 = df5.iloc[1:]





orders_new.drop(orders_new.loc[orders_new['address'] == 'Lviv, Lviv, Ukraine'].index, inplace = True)
orders_new = orders_new.dropna(subset = ['X'])

orders_neww = orders_new.dropna(subset = ['X'])

orders_neww['MAINCITY'].unique()


# There was a problem with the data where some of the X's were Y's and reverse. 
orders_newww = orders_neww

orders_newww.loc[orders_newww['MAINCITY'] !=1, 'X'] =orders_neww.loc[orders_neww['MAINCITY'] !=1, 'Y']
orders_newww.loc[orders_newww['MAINCITY'] !=1, 'Y'] = orders_neww.loc[orders_neww['MAINCITY'] !=1, 'X']



orders_new.loc[orders_new['MAINCITY'] != 1][['X', 'Y']].dropna(inplace = True)
orders_neww[['X', 'Y']]


orders_newww.loc[orders_newww['MAINCITY'] !=1, 'X']
orders_newww.loc[orders_newww['MAINCITY'] !=1, 'Y']

orders_newww

orders_newww.loc[orders_neww['MAINCITY'] !=1, 'Y']


# Here I start removing any data that doesn't fit into the geographic boundaries of Lviv. This removes and mistakes made by the geocoders data..
orders_new22 = orders_newww.drop(orders_newww.loc[(orders_newww['Y'] <= 49.5) | (orders_newww['Y'] >= 51.3)].index)
orders_new33 = orders_newww.drop(orders_newww.loc[(orders_newww['X'] <= 23.4) | (orders_newww['X'] >= 24.1)].index)



orders_neww
orders_neww.loc[(orders_neww['X'] <= 23.4) | (orders_neww['X'] >= 24.1)]
orders_new33
data = orders_new22.merge(orders_new33, how = 'inner')

data.to_csv('add_distances.csv')


#This is some code the cleans the ZDO data also. 

zdo = zdo.apply(lambda x: x.str.replace("'", ""))
zdo_columns = []
for k in zdo.columns:
    k = k.replace("'", "")
    zdo_columns.append(k)

zdo.columns = zdo_columns

zdo.to_csv('zdo_cleaned.csv')





