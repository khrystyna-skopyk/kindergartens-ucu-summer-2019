# this is some code for KMeans clustering for the data. 
from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np

df = pd.read_csv('distances_full2.csv')

cost = []

for k in range(25, 44):
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(df[['X', 'Y']])
    df[k] = kmeans.predict(df[['X', 'Y']])
    cost.append(kmeans.inertia_)

import matplotlib.pyplot as plt
plt.plot(np.arange(len(cost)), cost)
plt.show()

import os 
os.getcwd()
df.to_csv('C:\\Users\\DELL XPS\\Desktop\\Kindergarden Project\\data_not_useful\\kmeans_cluster.csv')
plt.plot(sums)
plt.show()

kmeans.cluster_centers_
df['X'].apply(lambda x: print(x))
help(df.apply)
kmeans.cluster_centers_[0]

