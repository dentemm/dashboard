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

    url(r'tasks/update/(?P<pk>\d+)/$', home_views.UpdateTaskModalView.as_view(), name='update-task-modal'),

    # Request views
    url(r'requests/new/tool/(?P<tool_id>\d+)/$', home_views.AddRequestModalView.as_view(), name='add-request-for-tool'),


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
