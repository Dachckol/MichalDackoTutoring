from django.contrib import admin
from generalinfo.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display = ("name","accepting","active")
	list_editable = ("accepting","active")

# Register your models here.
admin.site.register(Profile, ProfileAdmin)