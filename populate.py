import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from app.models import Layout, Place, Class
from datetime import datetime
from django.db import models

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    layoutImages = [
        {"name": "Square layout",
         "url":"media/layout_images/squareLayout.png"},
        {"name": "Angled layout",
         "url":"media/layout_images/angledLayout.png"}]

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
        {"name":"Bottle",
         "day":"http://bottlepy.org/docs/dev/",
         "views": 90},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views": 100} ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16} }

    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()