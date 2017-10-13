from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
	list_display=("title","target", "expired")
	list_editable=("expired",)

admin.site.register(Notification, NotificationAdmin)

