import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ClassMateZ.settings')

import django
django.setup()
from app.models import Layout, Place, Class, Zone
from datetime import datetime
from django.db import models

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    layouts = [
        {"name": "Square layout",
         "coords": "226,53,225,160,485,161,485,53;486,54,487,162,768,160,768,52;226,162,226,323,386,322,389,162;390,164,389,323,598,322,597,162;599,164,600,321,768,321,766,162;227,323,225,434,498,435,496,323;499,323,498,436,768,433,767,324",
         "url":"layout_images/squareLayout.png"},
        {"name": "Angled layout",
         "coords": "114,62,113,283,211,281;242,63,290,259,474,257,474,61;475,65,475,260,656,257,705,62;835,65,736,284,836,283;114,285,114,455,201,456,200,283;202,284,203,455,288,456,213,284;292,260,340,456,474,455,473,261;475,263,476,455,607,455,655,260;735,287,660,455,749,456,747,285;748,287,751,455,835,455,834,285",
         "url":"layout_images/angledLayout.png"}]

    places = [
        {"name":"Boyd Orr 222",
         "address":"Boyd Orr Building",
         "layout": "Angled layout"},
        {"name":"Adam Smith 1115",
         "address":"Adam Smith Building",
         "layout": "Angled layout"},
        {"name":"Adam Smith 718",
         "address":"Adam Smith Building",
         "layout": "Square layout"}]

    clases = [
        {"name":"ADS2",
         "day":1,
         "classId": "ads2-mon",
         "place": "Boyd Orr 222"},
        {"name":"Joose",
         "day":2,
         "classId": "Joose-tue",
         "place": "Adam Smith 1115"},
        {"name":"Embedded System",
         "day":3,
         "classId": "EMB-wed",
         "place": "Adam Smith 718"}
         ]


    for layout in layouts:
        add_layout(layout["name"], layout["coords"], layout["url"])
        print(layout["name"])

    for place in places:
        add_place(place["name"], place["address"], place["layout"])
        print(place["name"])

    for classToCreate in clases:
        add_class(classToCreate["name"], classToCreate["day"], classToCreate["place"], classToCreate["classId"])
        print(classToCreate["name"])

def add_layout(name, coords, url):
    l = Layout.objects.get_or_create(layoutName=name)[0]
    l.image=url
    l.zoneCoords=coords
    l.save()
    return l

def add_place(name, address, layout):
    Place.objects.get_or_create(name=name, address=address, layout=Layout.objects.get(layoutName=layout))

def add_class(name, day, place_name, classId):
    place = Place.objects.get(name=place_name)
    zoneCoords = place.layout.zoneCoords;
    zonesNum = len(zoneCoords.split(";"))
    Class.objects.get_or_create(name=name, day=day, place=Place.objects.get(name=place), classId = classId)
    zClass = Class.objects.get(name=name, day = day, place=place, classId = classId)
    for i in range(zonesNum):
        zone = Zone.objects.get_or_create(zClass = zClass, zoneNumber = i+1)
        print zone


# Start execution here!
if __name__ == '__main__':
    print("Starting ClassMateZ population script...")
    populate()