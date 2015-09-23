from django.conf.urls import patterns, include, url
from django.contrib import admin

from register.views import ReceptionView, DoctorView

urlpatterns = patterns('',
    url(r'^$', ReceptionView.as_view()),
    url(r'^doctor/(?P<id>\d+)/$', DoctorView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)
