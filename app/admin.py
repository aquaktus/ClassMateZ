from django.contrib import admin
from app.models import UserProfile
from app.models import Class
from app.models import Place
from app.models import Layout
from app.models import Zone

# Register your models here.

class ClassAdmin(admin.ModelAdmin):
	prepopulated_fields = {'classId':('name', str('time'), 'day')}

admin.site.register(UserProfile)
admin.site.register(Class, ClassAdmin)
admin.site.register(Place)
admin.site.register(Layout)
admin.site.register(Zone)