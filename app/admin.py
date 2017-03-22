from django.contrib import admin
from app.models import UserProfile
from app.models import Class
from app.models import Place

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Class)
admin.site.register(Place)