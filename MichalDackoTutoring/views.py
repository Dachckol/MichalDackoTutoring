from django.shortcuts import render
from generalinfo.models import Profile
from school.models import Level, Teacher


def home(request):
    template = "index.html"
    context={}
    return render(request,template,context)

def pricing(request):
    template = "pricing.html"
    context ={"levels":Level.objects.all()}
    return render(request,template,context)

def about(request):
	template = "about.html"
	context= {"teachers": Teacher.objects.all()}
	return render(request, template, context)