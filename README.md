# US State Department Data of Deaths by US Citizens Abroad

Data is from [here](http://travel.state.gov/law/family_issues/death/death_600.html)

The data is a little messy in the geographics.  I did some Levenshtein matches to 
sync it with ISO codes, but there a fair number of data irregularities that made things hard---
where Levs didn't match, I ran the address through googlemaps api, which did a pretty
good job of identifying the country.

Over the next couple of days, with my 1000 API calls per day, I'm going to go back to the original list
and record lat-longs.  

The most useful item in this repo is probably output/useful.csv

The source file is source/report.xls

There are several correspondences in the source folder from various ISO crosswalks---licenses
looked open source.  Please let me know if I got that incorrect from anyone.  (The ISO itself
will ask you to buy a copy of the standard, so definitely do that if you're considering commercial
use of of any of this.)

The code itself is pretty ugly---due in part to the API limitations of google maps meaning
Levenshteins were cheaper to run than API calls, but also due to data cleaning having a lot
of side effects, making imperative loops more necessary and clean functions trickier.  A lot
of this cleaning might have been easier in R.

This gives you: 

* /common/ country name
* ISO-3166-alpha-2
* ISO-3166-alpha-3
* Cause of Death
* Aggregated Cause of Death (so, all "Drowning" are together)
* Detail (For "Drowning - Canal", "Drowning - Ocean", the second part, only "Canal", "Ocean")

Travel safe.
