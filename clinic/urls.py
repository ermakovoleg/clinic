from django.conf.urls import patterns, include, url
from django.contrib import admin

from register.views import ReceptionView, doctorview

urlpatterns = patterns('',
    url(r'^$', ReceptionView.as_view()),
    url(r'^doctor/(?P<doctor_id>\d+)/$', doctorview),

    url(r'^admin/', include(admin.site.urls)),
)
