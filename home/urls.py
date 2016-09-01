from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^events/event/(?P<event_id>\d+)/$', views.TasksForEventApiView.as_view(), name='event-tasks'),
    url(r'^resources/event/(?P<event_id>\d+)/$', views.ResourcesForEventApiView.as_view(), name='event-resources'),
]