from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Session, Student, Teacher, Subject, Topic, Resource, Upload, Profile

class LoginForm(forms.Form):
	username=forms.CharField(label="Username", max_length=100)
	password=forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
	old_password=forms.CharField(label="Old Password", max_length=100, widget=forms.PasswordInput)
	new_password=forms.CharField(label="New Password", max_length=100, widget=forms.PasswordInput)
	reenter_password=forms.CharField(label="Reenter Password", max_length=100, widget=forms.PasswordInput)

	def clean(self):
		new_password=self.cleaned_data["new_password"]
		reenter_password=self.cleaned_data["reenter_password"]

		if new_password and new_password!=reenter_password:
			raise forms.ValidationError("The two entered passwords do not match. Please try again.")
		return self.cleaned_data

class CreateSessionForm(ModelForm):
	class Meta:
		model=Session
		fields=['student', 'teacher', 'subjects', 'date', 'duration', 'discount']

	student = forms.ModelChoiceField(queryset=Student.objects.all())
	teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
	subjects= forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
	date= forms.DateTimeField(input_formats=('%Y-%m-%dT%H:%MZ','%Y-%m-%dT%H:%M','%Y-%m-%d %H:%M', '%d/%m/%Y, %H:%M'))
	duration= forms.IntegerField()
	discount= forms.FloatField()

class ViewSessionForm(ModelForm):
	class Meta:
		model=Session
		fields=['notes','request','report','feedback','plannedTopics','learnedTopics']

	notes = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
	request = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
	report = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
	feedback = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
	plannedTopics= forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), required=False)
	learnedTopics=forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), required=False)

class AddTopicForm(ModelForm):
	class Meta:
		model=Topic
		fields=['name','subject']

	subject=forms.ModelChoiceField(queryset=Subject.objects.all())
	name= forms.CharField(max_length=100)

class AddResourceForm(ModelForm):
	class Meta:
		model=Resource
		fields=['name','link','description','topics']

	name=forms.CharField(max_length=100)
	link=forms.CharField(max_length=200)
	description=forms.CharField(max_length=500, widget=forms.Textarea)
	topics=forms.ModelMultipleChoiceField(queryset=Topic.objects.all())

class UploadFileForm(ModelForm):
	class Meta:
		model=Upload
		fields=['name', 'data', 'author']
	name=forms.CharField(max_length=50)
	data=forms.FileField()
	author=forms.ModelChoiceField(queryset=Profile.objects.all())
