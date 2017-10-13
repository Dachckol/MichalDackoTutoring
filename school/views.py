from django.shortcuts import render, redirect
from django.contrib.auth import logout as signout
from django.contrib.auth import login as signin 
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import QuerySet
from itertools import chain
from .models import Profile, Session, Topic, Resource, Upload
from .forms import LoginForm, ChangePasswordForm, CreateSessionForm, ViewSessionForm, AddTopicForm, AddResourceForm, UploadFileForm
from notifications.models import Notification

def home(request):
	if request.user.is_authenticated:
		return redirect('profile')
	else:
		return redirect('login')

def sudo(request,username):
	if not request.user.is_authenticated:
		return redirect('login')
	if not request.user.profile.isTeacher:
		return redirect('profile')
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		messages.add_message(request,messages.ERROR, "User does not exist!")
		return redirect('profile')
	if not request.user.is_superuser:
		if user.profile.isTeacher:
			messages.add_message(request,messages.ERROR, "You cannot log in as another teacher!")
			return redirect('profile')
	signin(request,user)
	return redirect('profile')

def login(request):
	if request.user.is_authenticated:
		return redirect('profile')
	template= "login.html"
	if request.method=="POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			user=authenticate(request,username=form.cleaned_data["username"], password=form.cleaned_data["password"])
			if user is not None:
				signin(request,user)
				return redirect('profile')
			else:
				form.add_error(None, "Username and password not recognised. Please try again.")
	else:
		form=LoginForm()
	context ={"form":form}
	return render(request,template,context)

def logout(request):
	if request.user.is_authenticated:
		signout(request)
	return redirect('/')

def profile(request):
	if not request.user.is_authenticated:
		return redirect('login')
	profile= Profile.objects.get(user=request.user)
	context={}
	if profile.isTeacher:
		template="teacherProfile.html"
		unPaidSessions = profile.Teacher.Sessions.all().filter(paid=False, done=True, completed=False).order_by("-changedForTeacher", "-date")
		DoneSessions= profile.Teacher.Sessions.all().filter(done=True, paid=True, completed=False).order_by("-changedForTeacher", "-date")
		unDoneSessions = profile.Teacher.Sessions.all().filter(done=False, completed=False).order_by("-changedForTeacher", "-date")
		context.update({"unPaidSessions":unPaidSessions, "DoneSessions":DoneSessions, "unDoneSessions":unDoneSessions})
	elif profile.isStudent:
		template="studentProfile.html"
		unDoneSessions = profile.Student.Sessions.all().filter(done=False, completed=False).order_by("-changedForStudent", "-date")
		DoneSessions= profile.Student.Sessions.all().filter(done=True, completed=False).order_by("-changedForStudent", "-date")
		context.update({"DoneSessions":DoneSessions, "unDoneSessions":unDoneSessions})
	elif profile.isParent:
		template="studentProfile.html"
		unDoneSessions = Session.objects.all().filter(done=False, completed=False,student__in=profile.Child.all()).order_by("-date")
		DoneSessions= Session.objects.all().filter(done=True, completed=False,student__in=profile.Child.all()).order_by("-date")
		context.update({"DoneSessions":DoneSessions, "unDoneSessions":unDoneSessions})
	context.update({"form":ChangePasswordForm(),"profile":profile})
	return render(request,template,context)

def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('login')
	template="changepassword.html"
	context={}
	if request.method=="POST":
		form=ChangePasswordForm(request.POST)
		if form.is_valid():
			user=authenticate(request,username=request.user.username, password=form.cleaned_data["old_password"])
			if user is not None:
				password=form.cleaned_data["new_password"]
				user.set_password(password)
				user.save()
				signin(request,user)
				messages.add_message(request,messages.SUCCESS, "Your password has been changed!")
				n=Notification(css="success", target=user.profile, expired=True, title='Password Changed', text='Your password on michaldackotutoring.co.uk has been changed!\n If you ever forget your password just contact me.')
				n.save()
				return redirect('profile')
			else:
				form.add_error(None, "Old password incorrect. Please try again.")
	else:
		form=ChangePasswordForm()
	context.update({"form":form})
	return render(request,template,context)

def viewsessions(request):
	if not request.user.is_authenticated:
		return redirect('login')
	template="viewsessions.html"
	context={}
	profile= Profile.objects.get(user=request.user)
	if profile.isParent:
		sessions=Session.objects.all().filter(completed=True,student__in=profile.Child.all()).order_by("-date")
	if profile.isTeacher:
		sessions=profile.Teacher.Sessions.all().filter(completed=True).order_by("-date")
	elif profile.isStudent:
		sessions=profile.Student.Sessions.all().filter(completed=True).order_by("-date")
	context.update({"sessions":sessions})
	return render(request,template,context)

def done(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	profile= Profile.objects.get(user=request.user)
	if not profile.isTeacher:
		return redirect('profile')
	try:
		session = Session.objects.get(id=id)
	except Session.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	if not session.teacher==profile.Teacher:
		messages.add_message(request,messages.ERROR, "Thats not your session!")
		return redirect('profile')
	session.done=True
	session.changedForStudent=True
	session.changedForTeacher=True
	session.save()
	n=Notification(
		title='Pending Changes In Session',
		text=profile.getName()+ ' has marked a session as done. This means you can now provide feedback and review your progress. Please mark the session complete once you are done.',
		target=session.student.profile,
		link="/school/session/"+str(id),
		css="warning"
		)
	n.save()
	messages.add_message(request, messages.SUCCESS, "Session done!")
	return redirect('profile')

def markpaid(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	profile= Profile.objects.get(user=request.user)
	if not profile.isTeacher:
		return redirect('profile')
	try:
		session = Session.objects.get(id=id)
	except Session.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	if not session.teacher==profile.Teacher:
		messages.add_message(request,messages.ERROR, "Thats not your session!")
		return redirect('profile')
	session.paid=True
	session.save()
	messages.add_message(request, messages.SUCCESS, "Session marked as paid!")
	n=Notification(
		title='Payment Confirmation',
		text="This is a confirmation of "+profile.getName()+ ' receiving the payment of £'+str(session.cost)+' for the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+".",
		target=session.student.parent,
		link="/school/session/"+id,
		css="success"
		)
	n.save()
	return redirect('profile')

def requestreview(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	profile= Profile.objects.get(user=request.user)
	if not profile.isParent:
		return redirect('profile')
	try:
		session = Session.objects.get(id=id)
	except Session.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	if not session.student.parent==profile:
		messages.add_message(request,messages.ERROR, "Thats not your session!")
		return redirect('profile')
	if (not session.done) or session.completed or session.paid:
		messages.add_message(request,messages.ERROR, "Session needs to be unpaid, done and uncompleted!")
		return redirect('/school/session/'+id)
	session.changedForTeacher=True
	n=Notification(
		title='Review Session Request',
		text=profile.getName()+ ' has requested a session review. This means the parent believes the session has been paid for.'+
			' Please check for an income of £'+str(session.cost)+' for the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+
			".\n\nPayment Reference: "+session.getReference(),
		target=session.teacher.profile,
		link="/school/session/"+id,
		css="warning"
		)
	n.save()
	messages.add_message(request,messages.SUCCESS, "Review request completed. The teacher will receive an email and a notification prompting them to check for the payment.")
	return redirect('/school/session/'+id)

def complete(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	profile= Profile.objects.get(user=request.user)
	try:
		session = Session.objects.get(id=id)
	except Session.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	if profile.isTeacher:
		if not session.teacher==profile.Teacher:
			messages.add_message(request,messages.ERROR, "That's not your session!")
			return redirect('profile')
		if session.changedForTeacher:
			messages.add_message(request,messages.ERROR, "Session cannot be marked complete as you have not reviewed the most recent changes! Please view the session first.")
			return redirect('profile')
		session.completedTeacher=True
		messages.add_message(request,messages.SUCCESS, "Session marked completed by teacher!")
	elif profile.isStudent:
		if not session.student.profile==profile:
			messages.add_message(request,messages.ERROR, "That's not your session!")
			return redirect('profile')
		if session.changedForStudent:
			messages.add_message(request,messages.ERROR, "Session cannot be marked complete as you have not reviewed the most recent changes! Please view the session first.")
			return redirect('profile')
		session.completedStudent=True
		messages.add_message(request,messages.SUCCESS, "Session marked complete by student!")
	else:
		messages.add_message(request,messages.ERROR, "Parents cannot mark sessions as complete!")
		return redirect('profile')
	session.save()
	return redirect('profile')

def view(request,id):
	if not request.user.is_authenticated:
			return redirect('login')
	profile= Profile.objects.get(user=request.user)
	try:
		session = Session.objects.get(id=id)
	except Session.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	if not profile == session.teacher.profile and not profile == session.student.profile and not profile == session.student.parent:
		messages.add_message(request,messages.ERROR, "This is not your session!")
		return redirect('profile')
	template="viewsession.html"
	if not request.method=="POST":
		sessionForm=ViewSessionForm()
		topicForm=AddTopicForm()
		uploadForm=UploadFileForm()
		if profile.isTeacher:
			session.changedForTeacher=False
		elif profile.isStudent:
			session.changedForStudent=False
	else:
		upload = Upload()
		uploadForm=UploadFileForm(request.POST, request.FILES, instance=upload)
		topic = Topic()
		topicForm=AddTopicForm(request.POST, instance=topic)
		s=Session.objects.get(id=session.id)
		sessionForm=ViewSessionForm(request.POST, instance=s)
		if uploadForm.is_valid() and not profile.isParent:
			upload = uploadForm.save()
			upload.save()
			session.uploads.add(upload)
			messages.add_message(request,messages.SUCCESS, "File uploaded!")
			target = Profile()
			if profile.isTeacher:
				target=session.student.profile
				session.changedForStudent=True
			else:
				target=session.teacher.profile
				session.changedForTeacher=True
			n=Notification(
				title='File Uploaded',
				text=profile.getName()+' has uploaded a file titled '+upload.name+' to a session on '+session.date.strftime("%d/%m/%Y at %H:%M")+'. Please have a look at it.',
				target=target,
				link="/school/session/"+str(id),
				css="warning"
				)
			n.save()
			topicForm=AddTopicForm()
			sessionForm=ViewSessionForm()
		elif topicForm.is_valid() and profile.isTeacher:
			topic = topicForm.save()
			session.plannedTopics.add(topic)
			session.save()
			messages.add_message(request,messages.SUCCESS, topic.name+" added to session and subject!")
			uploadForm=UploadFileForm()
			sessionForm=ViewSessionForm()
		elif sessionForm.is_valid():
			if not sessionForm.cleaned_data["plannedTopics"].first():
				sessionForm.cleaned_data["plannedTopics"] = session.plannedTopics.all()
			notes = sessionForm.cleaned_data["notes"]
			req = sessionForm.cleaned_data["request"]
			feedback = sessionForm.cleaned_data["feedback"]
			report= sessionForm.cleaned_data["report"]
			plannedTopics=sessionForm.cleaned_data["plannedTopics"]
			learnedTopics=sessionForm.cleaned_data["learnedTopics"]
			if (session.notes!=notes) or (session.report!=report) or (session.request!=req) or (session.feedback!=feedback) or session.plannedTopics.all().exclude(id__in=plannedTopics.all()) or session.learnedTopics.all().exclude(id__in=learnedTopics.all()):
				if profile.isTeacher:
					session.changedForStudent=True
					n=Notification(
						title='Session Changed',
						text=profile.getName()+ ' has changed the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+". Please review the changes they have made. "+
						"If the session has not happened yet, please do this as soon as possible. If you have marked the session as complete, you will need to do this again after reviewing the most recent changes.",
						target=session.student.profile,
						link="/school/session/"+str(id),
						css="warning"
						)
					n.save()
				elif profile.isStudent:
					session.changedForTeacher=True
					n=Notification(
						title='Session Changed',
						text=profile.getName()+ ' has changed the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+". Please review the changes they have made. "+
						"If the session has not happened yet, please do this as soon as possible. If you have marked the session as complete, you will need to do this again after reviewing the most recent changes.",
						target=session.teacher.profile,
						link="/school/session/"+str(id),
						css="warning"
						)
					n.save()
				else:
					session.changedForTeacher=True
					session.changedForStudent=True
					n=Notification(
						title='Session Changed',
						text=profile.getName()+ ' has changed the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+". Please review the changes they have made. "+
						"If the session has not happened yet, please do this as soon as possible. If you have marked the session as complete, you will need to do this again after reviewing the most recent changes.",
						target=session.teacher.profile,
						link="/school/session/"+str(id),
						css="warning"
						)
					n.save()
					n=Notification(
						title='Session Changed',
						text=profile.getName()+ ' has changed the session on '+session.date.strftime("%d/%m/%Y at %H:%M")+". Please review the changes they have made. "+
						"If the session has not happened yet, please do this as soon as possible. If you have marked the session as complete, you will need to do this again after reviewing the most recent changes.",
						target=session.student.profile,
						link="/school/session/"+str(id),
						css="warning"
						)
					n.save()
				messages.add_message(request,messages.SUCCESS, "Session updated!")
				print("here")
			session = sessionForm.save()
			uploadForm=UploadFileForm()
			topicForm=AddTopicForm()
	context={"session":session}
	if not session.done:
		topics = Topic.objects.filter(subject__in=session.subjects.all()).exclude(id__in=session.plannedTopics.all())
	else:
		topics = session.plannedTopics.all().exclude(id__in=session.learnedTopics.all())
	context.update({"sessionForm":sessionForm,"topicForm":topicForm, "uploadForm":uploadForm, "topics":topics})
	session.save()
	return render(request,template,context)

def create(request):
	if not request.user.is_authenticated:
		return redirect('login')
	profile=Profile.objects.get(user=request.user)
	if not profile.isTeacher:
		messages.add_message(request,messages.ERROR, "Only teachers can create sessions!")
		return redirect('profile')
	template="createsession.html"
	if request.method=="POST":
		s=Session()
		form=CreateSessionForm(request.POST, instance=s)
		if form.is_valid():
			s=form.save()
			n=Notification(
				title='Session Created',
				text=profile.getName()+ ' has created a new session on '+s.date.strftime("%d/%m/%Y at %H:%M")+". Please review it as soon as possible.",
				target=s.student.profile,
				link="/school/session/"+str(s.id),
				css="warning"
				)
			n.save()
			n=Notification(
				title='Session Created',
				text=profile.getName()+ ' has created a new session on '+s.date.strftime("%d/%m/%Y at %H:%M")+". If you wish to make any requests prior to the session, this is the time to do so.",
				target=s.student.parent,
				link="/school/session/"+str(s.id),
				css="warning"
				)
			n.save()
			return redirect('profile')
	else:
		form=CreateSessionForm()
		form.teacher= profile.Teacher
	context={"form":form, "students":profile.Teacher.Students}
	return render(request,template,context)

def topic(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	profile=Profile.objects.get(user=request.user)
	try:
		topic = Topic.objects.get(id=id)
	except Topic.DoesNotExist:
		messages.add_message(request,messages.ERROR, "Session does not exist!")
		return redirect('profile')
	resources = topic.Resources.filter(approved=True)
	template="viewtopic.html"
	context={"resources":resources, "topic":topic}
	if request.method=="POST":
		resource=Resource()
		form=AddResourceForm(request.POST, instance=resource)
		if form.is_valid():
			resource=form.save()
			resource.approved = profile.isTeacher
			resource.save()
			messages.add_message(request,messages.SUCCESS, "Resource added to topic(s)!")
			n=Notification(
				title="New Resource",
				text=profile.getName() + " has added a resource. Please review it.",
				target=Profile.objects.get(isTeacher=True, user__is_superuser=True),
				link="/school/topic/"+str(id),
				css="warning"
				)
			n.save()
	else:
		form=AddResourceForm()
	context.update({"form":form})
	return render(request,template,context)
	
