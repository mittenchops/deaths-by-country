#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
import subprocess
from pprint import pprint
import Levenshtein

deathtoll = []
with open('./output/locs.csv') as f:
    vals = csv.DictReader(f)
    for i in vals:
        deathtoll.append(i)

# This is not the best correspondence.  It has a lot of many to many
# and requires extra cleaning.  Australia and US Minor outlying islands
# in particular.
corr = []
with open('./source/iso_3166_2_countries_2.csv') as f:
    vals = csv.DictReader(f)
    for i in vals:
        corr.append(i)

for c in corr:
    if 'ISO3' not in c:
        c['ISO3'] = c.pop('ISO 3166-1 3 Letter Code')
    if 'ISO2' not in c:
        c['ISO2'] = c.pop('ISO 3166-1 2 Letter Code')

corr.append({'ISO2':"PS",'Common Name':'Palestine',"ISO3":'PSE'})
corr.append({'ISO2':"XZ",'Common Name':'International Waters',"ISO3":'XZ'})

def cleanjunk():
    for c in corr:
        if ((c['Common Name'] == 'Ashmore and Cartier Islands') or (c["Common Name"] == 'Coral Sea Islands') or (c['Common Name'] == 'Clipperton Island') or c["Common Name"] == 'Northern Cyprus'):
            print(c)
            corr.remove(c)
        if ((c['ISO2'] == "AU") and (c['Common Name'] != "Australia")):
            try:
                corr.remove(c)
            except:
                pass

# No idea why, but this needs to run > 4 times, so I made it a function.
cleanjunk(); cleanjunk(); cleanjunk(); cleanjunk(); cleanjunk()

for d in deathtoll:
    d['ISO3'] = d.get("ISO3",'')
    d['Name'] = d.get("Name",'')

for d in deathtoll:
    maxlev = 0
    for c in corr:
        if d['ISO'] == c['ISO2']:
            lev = Levenshtein.ratio(c["Common Name"].lower(),d['Country'].lower())
            if lev > maxlev:
                d['ISO3'] = c['ISO3']
                d['Name'] = c['Common Name']

matchfail = [w for w in deathtoll if w['ISO3']=='']

keys = deathtoll[0].keys()
keys.insert(0,keys.pop(-1))
with open('./output/full.csv', 'w') as f:
    wtr = csv.DictWriter(f, keys)
    wtr.writer.writerow(keys)
    wtr.writerows(deathtoll)

for d in deathtoll:
    d.pop('City')
    d.pop('Country')

for d in deathtoll:
    if 'COD' not in d:
        d['COD'] = d.pop('Cause of Death')
    if 'Agg' not in d:
        d['Agg'] = d['COD'].split(" - ")[0]
        d['Detail'] = d['COD'].split(" - ")[-1]

for d in deathtoll:
    if d['Detail'] == d['Agg']:
        d['Detail'] = ''

keys = deathtoll[0].keys()
keys.insert(0,keys.pop(-1))
with open('./output/useful.csv', 'w') as f:
    wtr = csv.DictWriter(f, keys)
    wtr.writer.writerow(keys)
    wtr.writerows(deathtoll)

