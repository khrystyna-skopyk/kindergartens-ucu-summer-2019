import pandas as pd 

df = pd.read_csv('zdo_cleaned.csv')
fact_2019 = pd.read_csv('fact_2019.csv')
fact_2018 = pd.read_csv('fact_2018.csv')

fact_2019 = fact_2019.apply(lambda x: x.str.replace("'", ""))
l = []
for k in fact_2019.columns:
    k = k.replace("'", "")
    l.append(k)

fact_2019.columns = l

fact_2018 = fact_2018.apply(lambda x: x.str.replace("'", ""))
l = []
for k in fact_2018.columns:
    k = k.replace("'", "")
    l.append(k)

fact_2018.columns = l

fact_2018

fact_2019['AMOUNT'] = pd.to_numeric(fact_2019['AMOUNT'])
fact_2018['AMOUNT'] = pd.to_numeric(fact_2018['AMOUNT'])

fact_2019['ZDO'] = pd.to_numeric(fact_2019['ZDO'])
fact_2018['ZDO'] = pd.to_numeric(fact_2018['ZDO'])



fact2019_grouped = fact_2019.groupby(["ZDO"])['AMOUNT'].sum()
fact2018_grouped = fact_2018.groupby(["ZDO"])['AMOUNT'].sum()

fact2018_grouped
fact2019_grouped


fact2019_grouped = fact2019_grouped.reset_index()
fact2018_grouped = fact2018_grouped.reset_index()

fact2018_grouped.sort_values('ZDO', ascending = True, inplace = True)
fact2019_grouped.sort_values('ZDO', ascending = True, inplace = True)



fact2019_grouped.index= fact2019_grouped['ZDO']
fact2018_grouped.index = fact2018_grouped['ZDO']

fact2019_grouped.drop(['ZDO'], axis = 1, inplace = True)
fact2018_grouped.drop(['ZDO'], axis = 1, inplace = True)

zdo.index = zdo['ID']

fact2019_grouped = fact2019_grouped.join(zdo[['latitude', 'longitude']])
fact2018_grouped = fact2018_grouped.join(zdo[['latitude', 'longitude']])

fact2018_grouped['2019 Acceptances'] = fact2019_grouped['AMOUNT']

fact2018_grouped.columns = ['index', '2018 Acceptances', 'lat', 'lon', '2019 Acceptances']

fact2018_grouped['change'] = fact2018_grouped['2019 Acceptances'] - fact2018_grouped['2018 Acceptances']

fact2018_grouped.to_csv('zdo_analysis.csv')