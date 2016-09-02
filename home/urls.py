from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^events/event/(?P<event_id>\d+)/$', views.TasksForEventApiView.as_view(), name='event-tasks'),
    url(r'^resources/event/(?P<event_id>\d+)/$', views.ResourcesForEventApiView.as_view(), name='event-resources'),

    url(r'^events/tool/(?P<tool_id>\d+)/$', views.ActivitiesForToolApiView.as_view(), name='tool-activities'),
    url(r'^resources/tool/(?P<tool_id>\d+)/$', views.ResourcesForToolApiView.as_view(), name='tool-resources'),
]