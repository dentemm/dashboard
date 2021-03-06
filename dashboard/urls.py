from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from search import views as search_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.contrib.wagtailapi import urls as wagtailapi_urls

from home import views as home_views

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^api/', include('home.urls')),

    # HOME views

    # Task views
    url(r'tasks/new/$', home_views.AddTaskModalView.as_view(), name='add-task-modal'),
    url(r'tasks/new/event/(?P<event_id>\d+)/$', home_views.AddTaskModalView.as_view(), name='add-task-for-event'),
    url(r'tasks/new/tool/(?P<tool_id>\d+)/$', home_views.AddTaskModalView.as_view(), name='add-task-for-tool'),

    url(r'tool/calendarevent/(?P<pk>\d+)/$', home_views.CalendarEventModalViewTask.as_view(), name='tool-calendar-modal-task'),
    url(r'tool/calendarevent/(?P<event_slug>[\w-]+)/$', home_views.CalendarEventModalViewEvent.as_view(), name='tool-calendar-modal-event'),
    url(r'updatetasks/event/(?P<event_id>\d+)$', home_views.UpdateTasksForEventView.as_view(), name='update-tasks-for-event'),
    url(r'updatetasks/tool/(?P<tool_id>\d+)$', home_views.UpdateTasksForToolView.as_view(), name='update-tasks-for-tool'),

    # Request views
    url(r'requests/new/tool/(?P<tool_id>\d+)/$', home_views.AddRequestModalView.as_view(), name='add-request-for-tool'),
    url(r'requests/update/reject/(?P<pk>\d+)/$', home_views.RejectRequestUpdateView.as_view(), name='update-reject-request'),
    url(r'requests/update/plan/(?P<pk>\d+)/$', home_views.PlanRequestUpdateView.as_view(), name='update-plan-request'),
    url(r'requests/updat/accapt/(?P<pk>\d+)/$', home_views.AcceptRequestUpdateView.as_view(), name='update-accept-request'),
    url(r'requests/update/(?P<pk>\d+)/$', home_views.RequestUpdateView.as_view(), name='update-request'),

    # Event views
    url(r'events/new/tool/(?P<tool_id>\d+)/$', home_views.AddEventModalView.as_view(), name='add-event-for-tool'),
    


    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
