from django.contrib import admin
from .models import Officer
from .models import AccidentFiles
from django.contrib.auth.admin import UserAdmin



# Register your models here.
class OfficerAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'police_number', 'national_id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'police_number', 'national_id')

admin.site.register(Officer, OfficerAdmin)
admin.site.register(AccidentFiles)

