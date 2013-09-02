#!/bin/bash

wget "http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip"
unzip ne_50m_admin_0_countries.zip
#ogr2ogr -f "GeoJSON" output_features.json ne_50m_admin_0_countries.shp
ogr2ogr -f "GeoJSON" output_features.json ne_50m_admin_0_countries.shp -select iso_a3
topojson -o topoed.json output_features.json --id-property iso_a3

