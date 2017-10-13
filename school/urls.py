from django.conf.urls import include, url
from school import views as school


urlpatterns = [
    # Examples:
    url(r'^$', school.home, name='school_home'),
    url(r'^login/$', school.login, name='login'),
    url(r'^logout/$', school.logout, name='logout'),
    url(r'^profile/$', school.profile, name='profile'),
    url(r'^changepassword/$', school.changepassword, name='changepassword'),
    url(r'^viewsessions/$', school.viewsessions, name='viewsessions'),
    url(r'^sudo/(?P<username>\w+)/$', school.sudo, name='sudo'),
    url(r'^done/([0-9]+)/$', school.done, name='done'),
    url(r'^markpaid/([0-9]+)/$', school.markpaid, name='markpaid'),
    url(r'^complete/([0-9]+)/$', school.complete, name='complete'),
    url(r'^session/([0-9]+)/$', school.view, name='view'),
    url(r'^session/([0-9]+)/requestreview$', school.requestreview),
    url(r'^create/$', school.create, name="create"),
    url(r'^topic/([0-9]+)/$', school.topic, name="topic")
]
