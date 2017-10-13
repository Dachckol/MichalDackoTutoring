from django.contrib import admin
from .models import Profile, Student, Level, Subject, Topic, Session, Resource, Teacher, Upload

class ProfileAdmin(admin.ModelAdmin):
	def get_name(self, obj):
		return obj.user.username

	list_display = ("get_name","isStudent","isTeacher","isParent")

class StudentAdmin(admin.ModelAdmin):
	list_display = ("profile","parent")

class TeacherAdmin(admin.ModelAdmin):
	list_display = ("profile",)

class LevelAdmin(admin.ModelAdmin):
	list_display=("name","price")
	list_editable=("price",)

class SubjectAdmin(admin.ModelAdmin):
	list_display=("name","level")

class TopicAdmin(admin.ModelAdmin):
	list_display=("name","subject")

class SessionAdmin(admin.ModelAdmin):
	list_display=("date", "student","teacher","done","paid","completedTeacher","completedStudent","completed")
	list_editable=("done","paid","completedTeacher","completedStudent","completed")

class ResourceAdmin(admin.ModelAdmin):
	list_display=("name","approved","link","description")
	list_editable=("approved",)

class UploadAdmin(admin.ModelAdmin):
	list_display=("name","author")


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Upload,UploadAdmin)