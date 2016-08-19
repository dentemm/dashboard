from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.OverviewView.as_view(), name='overview'),
]