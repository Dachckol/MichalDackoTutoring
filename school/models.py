from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	isStudent = models.BooleanField(default=True)
	isParent = models.BooleanField(default=False)
	isTeacher = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def getName(self):
		return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance,created,**kwargs):
	instance.profile.save()

class Teacher(models.Model):
	profile=models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="Teacher")

	accountName=models.CharField(max_length=50)
	sortCode=models.CharField(max_length=8)
	accountNumber=models.CharField(max_length=8)

	about = models.TextField(max_length=1000)
	qualifications = models.TextField(max_length=500)
	picturelink = models.CharField(max_length=300)

	def __str__(self):
		return self.profile.getName()

class Student(models.Model):
	profile=models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="Student")
	parent=models.ForeignKey(Profile, related_name="Child")
	teacher= models.ForeignKey(Teacher, related_name="Students")

	def __str__(self):
		return self.profile.getName()

class Level(models.Model):
	name=models.CharField(max_length=100)
	note=models.TextField(max_length=500)
	price=models.FloatField()
	recommended=models.TextField(max_length=500)

	def __str__(self):
		return self.name 

class Subject(models.Model):
	name=models.CharField(max_length=100)
	level=models.ForeignKey(Level, related_name="Subjects")

	def __str__(self):
		return self.level.name + " " + self.name

class Topic(models.Model):
	name=models.CharField(max_length=100)
	subject=models.ForeignKey(Subject, related_name="Topics")

	def __str__(self):
		return self.name +" "+self.subject.level.name+ " " +self.subject.name

class Upload(models.Model):
	author = models.ForeignKey(Profile, related_name="Uploads")
	name = models.CharField(max_length=50)
	data = models.FileField(upload_to="uploads/"+str(datetime.now().year)+"/"+str(datetime.now().month))

	def __str__(self):
		return self.name


class Session(models.Model):
	subjects=models.ManyToManyField(Subject, related_name="Sessions")
	teacher=models.ForeignKey(Teacher, related_name="Sessions", null=True)
	student=models.ForeignKey(Student, related_name="Sessions")
	done=models.BooleanField(default=False)
	date=models.DateTimeField()
	duration=models.IntegerField()
	cost=models.FloatField(blank=True, null=True)
	notes=models.TextField(max_length=500, blank=True)
	request=models.TextField(max_length=1000, blank=True)
	report=models.TextField(max_length=500,blank=True)
	feedback=models.TextField(max_length=500,blank=True)
	paid=models.BooleanField(default=False)
	discount=models.FloatField(default=0)
	uploads=models.ManyToManyField(Upload, related_name="Sessions", blank=True)

	completedTeacher=models.BooleanField(default=False)
	completedStudent=models.BooleanField(default=False)
	completed=models.BooleanField(default=False)

	changedForTeacher=models.BooleanField(default=True)
	changedForStudent=models.BooleanField(default=True)

	plannedTopics=models.ManyToManyField(Topic, related_name="SessionsPlanned", blank=True)
	learnedTopics=models.ManyToManyField(Topic, related_name="SessionsLearned", blank=True)
	unlearnedTopics=models.ManyToManyField(Topic, related_name="SessionsFailed", blank=True)
	
	def getReference(self):
		return self.student.profile.user.first_name + " " + str(self.id)

	def save(self, *args, **kwargs):
		if self.done:
			self.cost=((self.duration/60)*self.subjects.all()[0].level.price)-self.discount
		if self.completedTeacher:
			if not self.changedForTeacher:
				if self.completedStudent:
					if not self.changedForStudent:
						if self.paid:
							self.completed=True
							self.unlearnedTopics = self.plannedTopics.all().exclude(id__in=self.learnedTopics.all())
					else:
						self.completedStudent=False
			else:
				self.completedTeacher=False
		if self.completedStudent and self.changedForStudent:
			self.completedStudent=False
		super(Session, self).save(*args, **kwargs)

class Resource(models.Model):
	name = models.CharField(max_length=100)
	link = models.URLField()
	description = models.TextField(max_length=200)
	topics = models.ManyToManyField(Topic, related_name="Resources",blank=True)
	approved= models.BooleanField(default=False)

	def __str__(self):
		return self.name