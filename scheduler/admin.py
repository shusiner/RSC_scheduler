from django.contrib import admin
from .models import Guard, Manager, Site, Schedule
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

#admin.site.register(Guard)
#admin.site.register(Manager)
#admin.site.register(Site)
#admin.site.register(Schedule)

# Define the admin class
class GuardAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'age', 'position', 'date_of_birth', 'site')
    list_filter = ('gender', 'date_of_birth')

# Register the admin class with the associated model
admin.site.register(Guard, GuardAdmin)

# Register the Admin classes for Manager using the decorator
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

# Register the Admin classes for Site using the decorator
@admin.register(Site) 
class SiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

@admin.register(Schedule) 
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('guard','date', 'is_day', 'is_night')
