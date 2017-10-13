from django.conf.urls import include, url
from django.contrib import admin
from MichalDackoTutoring import views as mdt_views
from testimonials import views as tes_views

urlpatterns = [
    # Examples:
    url(r'^$', mdt_views.home, name='home'),
    url(r'^pricing/$', mdt_views.pricing, name='pricing'),
    url(r'^testimonials/$', tes_views.testimonials, name='testimonials'),
    url(r'^about/$', mdt_views.about, name='about'),
    url(r'^school/', include('school.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
