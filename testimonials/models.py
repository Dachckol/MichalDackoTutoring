from django.db import models
from school.models import Teacher


class Testimonial(models.Model):
    subject = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    time = models.CharField(max_length=50)
    date = models.DateField()
    priority = models.IntegerField(default=100)
    teacher= models.ForeignKey(Teacher, related_name="Testimonials")

    def __unicode__(self):
        return self.subject
    def __str__(self):
        return self.subject
