from __future__ import unicode_literals
#from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Layout(models.Model):
    layoutName = models.CharField(max_length=100, default='New Layout', blank=False)
    nbrOfZones = models.IntegerField(default=0)
    image = models.ImageField(upload_to='layout_images')
    def __str__(self):
		return self.layoutName


class Place(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=100);
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    DAY = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )
    day = models.CharField(
        max_length=3,
        choices=DAY,
        default='mon',
        blank=False,
    )
    time = models.TimeField(default=datetime.strptime('00', '%H'), blank=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
		return self.name + " " + str(self.time) + " " + self.day
	#def __unicode__(self):
		#return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(max_length=100, default='new user', blank=False)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	classes = models.ManyToManyField(Class, blank=True)

	def __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.name

class Zone(models.Model):

    users = models.ManyToManyField(UserProfile, blank=True)
    zoneNumber = models.IntegerField(default=0)
    zClass = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self):
		return "Zone: " + str(self.zoneNumber) + " " + str(self.zClass)

	#def __unicode__(self):
		#return (self.class_id + ", " + self.layout)
