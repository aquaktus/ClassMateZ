from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	name = models.CharField(max_length=100)
	id = models.AutoField(primary_key=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	classes = models.ManyToManyField(Class)
	def __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.name

class Class(models.Model):

    name = models.CharField(max_length=100, primary_key=True)
    date = models.DateField()
    def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

class Place(models.Model):

    name = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=100);
    classes = models.ManyToManyField(Class)
    layout = models.ImageField(upload_to='layout_images')
    def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

Class Layout(models.Model):

    class_id = models.ForeignKey(Class, primary_key = True, on_delete=models.CASCADE)
    place_name = models.ForeignKey(Place, primary_key = True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='layout_images')
    def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name


class Zone(models.Model):
    ZONE_NAMES = (
        ('A', 'Zone A'),
        ('B', 'Zone B'),
        ('C', 'Zone C'),
    )
    id = models.CharField(max_length=1, primary_key=True)
    layout = models.ForeignKey= (Layout, primary_key = True, on_delete=models.CASCADE)
    users = ManyToManyField(UserProfile)
    def __str__(self):
		return self.class_id + ", " + layout

	def __unicode__(self):
		return self.class_id + ", " + layout






