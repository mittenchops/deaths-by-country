#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
import subprocess
from pprint import pprint
import Levenshtein
from geopy import geocoders
from config import YAHOOID

# via http://www.iso.org/iso/country_codes
tab = requests.get('http://www.iso.org/iso/home/standards/country_codes/country_names_and_code_elements_txt.htm')

corresp = []
for line in tab.iter_lines():
    print(line.split(";"))
    try:
        name, code = line.split(";") 
        corresp.append(dict(name=name, code=code))
    except:
        print("couldn't read{}".format(line.split(";")))

# via https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2, http://www.unece.org/cefact/locode/unlocode_manual.pdf
corresp.append(dict(name="INTERNATIONAL WATERS", code="XZ"))
corresp.append(dict(name="Netherlands Antilles",code="AN"))

with open('./source/corresp.csv','w') as f:
    wtr = csv.writer(f, dialect="excel")
    for c in corresp:
        try:
            code = c['code']
            name = c['name']
            wtr.writerow([code, name])
        except:
            print('FAILED TO WRITE',r)

subprocess.call("ssconvert ./source/report.xls ./source/report.csv", shell=True)

deathtoll = []
with open('./source/report.csv') as f:
    vals = csv.DictReader(f)
    for i in vals:
        deathtoll.append(i)

for d in deathtoll:
    d['Country'] = d["City"].rstrip(",.").split(",")[-1].strip()

gmap = geocoders.GoogleV3()
ymap = geocoders.Yahoo(YAHOOID)

def city2country(x):
    try:
        gres = gmap.geocode(x)
    except:
        gres = ''
    if gres:
        try:
            place = gres[0].split(",")[-1]
        except:
            place = ''
    else:
        try:
            yres = ymap.geocode(x)
            place = yres[0].split(",")[-1]
        except:
            place = ''
    country = str(place.strip())
    return(country)

countryreps = {
"Paktika" : "Afghanistan",
"Barbuda" : "Antigua and Barbuda",
'Western Australia Australia' : "Australia",
"South Australia" : "Australia",
'South Austalia' : "Australia",
'Western Australia' : "Australia",
'New South Wales': "Australia",
'Tasmania Australia' : "Australia",
"Aghanistan" : "Afghanistan",
'Great Northern Highway Derby Western Australia': "Australia",
'Baden. Austria' : "Austria",
"Neusiedl/zaya" : "Austria",
'The Bahamas': "Bahamas",
"Turks & Caicos":"Turks and Caicos Islands",
"San Salvador" : "Bahamas",
"Eleuthera" : "Bahamas",
"Nassau" : "Bahamas",
"bimini" : "Bahamas",
"abaco" : "Bahamas",
"Abaco" : "Bahamas",
"Freeport" : "Bahamas",
"British Virgin Islands":'Virgin Islands, British',
"British West Indies": "Turks and Caicos Islands",
"Bolivia": "Bolivia, Plurinational State Of",
"Between English Caye And Turneffe Reef" : "International Waters",
"Teakettle Village, Cayo District" : "Belize",
"Cayo District" : "Belize",
"Orange Walk Town": "Belize",
"San Pedro Town": "Belize",
"St. Lucia":"Saint Lucia",
"Antigua": "Antigua and Barbuda",
"Boliviz" : "Bolivia, Plurinational State Of",
"Santa Cruz": "Bolivia, Plurinational State Of",
"Palapye":"Botswana",
"Rn Brazil" : "Brazil",
"Phnom Penh": "Cambodia",
"Sihanoukville": "Cambodia",
"Littoral": "Cameroon",
"British Columbia": "Canada",
"Quebec": "Canada",
"Grand Cayman": "Cayman Islands",
"Sichuan": "China",
"Shanghai":"China",
"Guangdong": "China",
"Heilongjiang":"China",
"Inner Mongolia":"China",
"Sangha":"China",
"Congo-Kinshasa":"Congo, The Democratic Republic Of The",
"Bas-congo":"Congo, The Democratic Republic Of The",
"Aguirre":"Costa Rica",
"San Isidro Del General San Jose":"Costa Rica",
"Ivory Coast": "CÔTE D'IVOIRE",
"Havana":"Cuba",
"Pinar Del Rio" : "Cuba",
"Santo Domingo" : "Dominican Republic",
"La Altagracia" : "Dominican Republic",
"Rio San Juan": "Dominican Republic",
"Puerto Plata": "Dominican Republic",
"Galapagos": "Ecuador",
"Daule" : "Ecuador",
"Azuay": "Ecuador",
"Esmeraldas": "Ecuador",
"Cairo": "Egypt",
"130 Km Far From Addis Ababa" : "Ethiopia",
"sigatoka": "Fiji",
"lautoka": "Fiji",
"Tahiti": 'French Polynesia',
"Nice 06000": "France",
"46250 Gindou":"France",
"Paris 75007":"France",
'Brazil- North 02? 58\'8" /west 030? 35\'4"':"Brazil",
"The Gambia" : "Gambia",
"89584 Ehingen (donau)": "Germany",
"Bonn" : "Germany",
"Frankfurt Am Main": "Germany",
"67655 Kaiserslautern" : "Germany",
"Retalhuleu" : "Guatemala",
"Gressier Haiti": "Haiti",
"Bay Islands Honduras": "Honduras",
"Santa Barbara" : "Honduras",
"Cortes": "Honduras",
"Intibuca": "Honduras",
"Atlantida":"Honduras",
"Francisco Moranzan": "Honduras",
"Reykjavik": "Iceland",
"Ahmedabad 380 007 Gujarat": "India",
"Mumbai": "India",
"Iran":"Iran, Islamic Republic Of",
"Baghdad":"Iraq",
"Between Fallujah And Baghdad":"Iraq",
"Southern Iraq":"Iraq",
"Mayo":"Ireland",
"Kerry":"Ireland",
"Jerusalem":"Israel",
"The West Bank":'Palestine, State Of', #!!!
"Gaza":"Palestine, State Of",
"Northern Israel": "Israel",
"Nothern Israel": "Israel",
"Mougins":"France",
"West Bank":'Palestine, State Of',
"Foggia": "Italy",
"Massino Visconti, Novara, A26 Km 177":"Italy",
"Negril. Jamaica":"Jamaica",
"Osaka Japan":"Japan",
"Atyrau":"Kazakhstan",
"Korea":'Korea, Republic Of',
"South Korea":'Korea, Republic Of',
"North Korea":"Korea, Democratic People'S Republic Of",
"A26 Km 177": "Italy",
"Taebaek":'Korea, Republic Of',
"Seoul":'Korea, Republic Of',
"Shaab Al Bahri":"Kuwait",
"Um Qasr Iraq/kuwait Border": "Kuwait",
"Laos":"Lao People's Democratic Republic",
"Loas":"Lao People's Democratic Republic",
"Sam Neua Laos": "Lao People'S Democratic Republic",
"Macedonia":"Macedonia, The Former Yugoslav Republic Of",
"Kosovo": "Serbia", #!!!
"North Lebanon": "Lebanon",
"The Lebanese-syrian Border": "Lebanon",
"South Lebanon":"Lebanon",
"Nouakchott":"Mauritania",
"Tamaulipas":"Mexico",
"Baja California":"Mexico",
"Guerrero":"Mexico",
"Quintana Roo":"Mexico",
"Chihuahua":"Mexico",
"Sonora":"Mexico",
"BC":"Mexico",
"Michoacan":"Mexico",
"Jalisco":"Mexico",
"Baja California Sur":"Mexico",
"Nuevo Leon":"Mexico",
"San Luis Potosi":"Mexico",
"Zacatecas":"Mexico"}

countryreps.update(
{
"Oax" : "Mexico",
"Nayarit" : "Mexico",
"Coahuila" : "Mexico",
"Oaxaca":"Mexico",
"Mich": "Mexico",
"Gto":"Mexico",
"Colima":"Mexico",
"Mich. Mexico":"Mexico",
"pue. Mexico":"Mexico",
"Ver. Mexico":"Mexico",
"Gro. Mexico":"Mexico",
"Mex":"Mexico",
"Sonora Mexico":"Mexico",
"baja California":"Mexico",
"san Luis Potosi":"Mexico",
"D.f":"Mexico",
"Mina Nuevo Leon":"Mexico",
"Qunitana Roo":"Mexico", # typo
"Sinaloa":"Mexico",
"Sinola": "Mexico",
"Tamps": "Mexico",
"Mulege Baja California":"California",
"Az" : "Mexico",
"Micronesia":'Micronesia, Federated States Of',
"Moldova": "Moldova, Republic Of",
"Nethrland Antilles":"Netherland Antilles",
"Caribbean Netherlands":"Netherland Antilles",
"Caracao Netherlands Antilles":"Netherland Antilles",
"Sint Maarten":"Netherland Antilles",
"Russia":"Russian Federation",
"Cupecoy Beach":"Netherland Antilles",
"Haarlemmermeer":"Netherlands",
"Maroa":"Netherlands",
"Esteli": "Nicaragua",
"Managua":"Nicaragua",
"Nigeria (offshore)":"International Waters",
"Off The Coast Of Nigeria":"International Waters",
"4291 Kopervik":"Norway",
"Muzaffarabad":"Pakistan",
"620000":"Russian Federation",
"Carretera #15 Mexico- Nogales Sonora Km 176+350":"Mexico",
"Federated States of Micronesia":"Micronesia, Federated States of",
"Udhailiyah Saudi Arabia":"Saudi Arabia",
"Dhahran Saudi Arabia":"Saudi Arabia",
"Serbia And Montenegro":"Serbia",
"UK":"United Kingdom",
"Uk":"United Kingdom",
"England":"United Kingdom",
"Scotland":"United Kingdom",
"USVI":"Trinidad and Tobago",
"Thai":"Thailand",
"Tanzania":'Tanzania, United Republic Of',
"Phuket Thailand":"Thailand",
"Tibet Autonomous Region": "China",
"Choyu, Nyalam, Tibet Autonomous Region":"China",
"Taiwan":"Taiwan, Province of China",
"Taiwan 900":"Taiwan, Province of China",
"Taiwan 251":"Taiwan, Province of China",
"Taiwan 242":"Taiwan, Province of China",
'Taiwan 950':"Taiwan, Province of China",
"Venezuela": "Venezuela, Bolivarian Republic Of",
"Syria": "Syrian Arab Republic",
"Chaguaramas":"Trinidad and Tobago",
"Mulege Baja California":"Mexico",
"The Netherlands":"Netherlands",
"Valencia":"Spain",
"Antilles":"Netherlands Antilles",
"Maroa":"New Zealand",
"Banglamung Chon Buri":"Thailand",
"Trinidad":"Trinidad and Tobago",
"Tobago":"Trinidad and Tobago",
"Bunya County Busoga Province":"Uganda",
"Khanh Hoa":"Vietnam"
}
)

def mapreplace(x,disc):
    try:
        return([v for k,v in disc.items() if x == k][0])
    except:
        return(None)

for d in deathtoll:
    val = mapreplace(d['Country'],countryreps)
    if val:
        d['Country'] = val

for d in deathtoll:
    d['ISO'] = d.get("ISO","")

def matchiso(deathtoll, ratio=0.75):
    for d in deathtoll:
        maxlev = 0
        for c in corresp:
            lev = Levenshtein.ratio(d["Country"].lower(),c['name'].lower())
            # Consider Levenshtein.ratio("Australia","Austria") == 0.875
            if (lev > maxlev) and (lev > ratio):
                maxlev = lev
                d['ISO'] = c['code']

matchiso(deathtoll,0.9)

for d in deathtoll:
    if d['ISO'] == '':
        try:
            val = city2country(d['City'])
            if val:
                d['Country'] = val
        except:
            pass

matchiso(deathtoll,0.5)

for d in deathtoll:
    val = mapreplace(d['Country'],countryreps)
    if val:
        d['Country'] = val

matchiso(deathtoll,0.5)

deathtoll = [w for w in deathtoll if w["City"]!='']

with open('./output/locs.csv','w') as f:
    wtr = csv.writer(f, dialect="excel")
    wtr.writerow(["Date","City","Cause of Death","ISO","Country"])
    for c in deathtoll:
        try:
            date = c['Date']
            city = c['City']
            cod = c['Cause of Death']
            ISO = c['ISO']
            country = c['Country']
            wtr.writerow([date, city, cod, ISO, country])
        except:
            print('FAILED TO WRITE',r)


matchfail = [w for w in deathtoll if w['ISO']=='']
matched = [w for w in deathtoll if w['ISO']!='']

len(matchfail)
pprint(matchfail[0:10])

#t = set(d['Country'] for d in deathtoll) 
#t = set(d['City'] for d in deathtoll) 
