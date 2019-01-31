# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:11:39 2019

@author: maehu
"""

import pandas as pd
import re

f = open("new-york-city-transport-statistics/mta_1712.csv", "r")
lines = f.readlines()
f.close()


temp = open("new-york-city-transport-statistics/mta_1712_new.csv", "w")
for l in lines:
    x = re.search("non-public,for GEO", l)
    if x:
        l = l[:x.span()[0]] + "non-public for GEO" + l[x.span()[1]:]
    temp.write(l)
temp.close()
del(lines, l, x)

data = pd.read_csv("new-york-city-transport-statistics/mta_1712_new.csv")


data.rename(index=str, inplace=True,
               columns={"VehicleLocation.Latitude": "vehicle_latitude",
                                   "VehicleLocation.Longitude": "vehicle_longitude"})
data['RecordedAtTime'] = pd.to_datetime(data['RecordedAtTime'])
data['DirectionRef'] = data['DirectionRef'].astype('category')
data['PublishedLineName'] = data['PublishedLineName'].astype('category')

routes = data.PublishedLineName.values
burrow_routes = list()
for r in routes:
    burrow_routes.append(re.split('(\d+)',r)[0])
del(r)
    
data['burrow_route'] = burrow_routes
data['burrow_route'] = data['burrow_route'].astype('category')
del(burrow_routes)

data.to_pickle("new-york-city-transport-statistics/mta1712.pkl")
data_small = data[['VehicleRef', 'RecordedAtTime', 'vehicle_latitude',
       'vehicle_longitude', 'PublishedLineName', 'burrow_route']]
data_small.to_pickle("new-york-city-transport-statistics/mta1712_small.pkl")
del(data)
del(data_small)


# change name
data = pd.read_pickle("new-york-city-transport-statistics/mta1706.pkl")
data.rename(index=str, inplace=True,columns={"bur_routes": "burrow_route"})
data.to_pickle("new-york-city-transport-statistics/mta1706.pkl")
# add burrow route to small
data_small = pd.read_pickle("new-york-city-transport-statistics/mta1706_small.pkl")
data_small['burrow_route'] = data.burrow_route
data_small.to_pickle("new-york-city-transport-statistics/mta1706_small.pkl")
