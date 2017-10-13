from django.contrib import admin
from testimonials.models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("subject","level","date","priority")
	list_editable = ("priority",)

admin.site.register(Testimonial, TestimonialAdmin)
