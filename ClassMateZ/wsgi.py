"""
WSGI config for ClassMateZ project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
# This file contains the WSGI configuration required to serve up your
# web application at http://wad2.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#


import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/peopleofcs/ClassMateZ'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClassMateZ.settings")

application = get_wsgi_application()