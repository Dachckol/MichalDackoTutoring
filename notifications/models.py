from django.db import models
from school.models import Profile
from django.db.models.signals import post_init
from django.core.mail import send_mail


class Notification (models.Model):
	target=models.ForeignKey(Profile, related_name="notifications")
	text=models.TextField(max_length=500)
	hasLink=models.BooleanField(default=False)
	link=models.CharField(max_length=100)
	title=models.CharField(max_length=50)
	css=models.CharField(max_length=10)

	expired=models.BooleanField(default=False)
	emailed=models.BooleanField(default=False)

	def __str__(self):
		return self.title

def createNotification(**kwargs):
	instance=kwargs.get("instance")
	if instance.text=="":
		return
	if Notification.objects.all().filter(expired=False, text=instance.text).exclude(id=instance.id).count()>0:
		instance.expired=True
		instance.save()
		return
	instance.hasLink= not instance.link == ""
	if not instance.emailed and not instance.expired:
		send_mail(instance.title, "Hello,\n\n"+instance.text+"\n\nKind Regards,\n\nRobot Michal", "dackomichal@gmail.com", [instance.target.user.email], fail_silently=True)
		instance.emailed=True
		print("emailed")
	instance.save()
post_init.connect(createNotification,Notification)


