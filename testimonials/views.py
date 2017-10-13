from django.shortcuts import render
from generalinfo.models import Profile
from testimonials.models import Testimonial


def testimonials(request):
    template = "testimonials.html"
    context = Profile.objects.filter(active=True)[0].getContext()
    reviews = Testimonial.objects.all().order_by("priority")
    context.update({"reviews":reviews})
    return render(request,template,context)