from __future__ import absolute_import, unicode_literals

from django.db import models as djangomodels
from django.conf import settings

from wagtail.wagtailcore import models
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey

@register_snippet
class Task(djangomodels.Model):

	title = djangomodels.CharField(max_length=63)
	description = djangomodels.CharField(max_length=510)
	owner = djangomodels.ForeignKey(settings.AUTH_USER_MODEL)

	page = ParentalKey('home.SafeWorkingPermit', related_name='tasks')

Task.panels = [
	
	FieldPanel('title'),
	FieldPanel('description')
]

class SafeWorkingPermit(models.Page):

	vwv_owner = djangomodels.ForeignKey(settings.AUTH_USER_MODEL)
	vwv_title = djangomodels.CharField(max_length=63)
	description = djangomodels.CharField(max_length=510)

# Panel definitions for SafeWorkingPermit page
SafeWorkingPermit.content_panels = models.Page.content_panels + [

	FieldPanel('title'),
	InlinePanel('tasks', label='Tasks')
]


class SafeworkingPermitUser(djangomodels.Model):

	user = djangomodels.ForeignKey(settings.AUTH_USER_MODEL)
	page = ParentalKey('home.SafeWorkingPermit', related_name='involved_parties')
	role = djangomodels.CharField(max_length=8) # Welke rol heeft deze gebruiker voor een gegeven Veilig Werk Vergunning?

	



class ToolPage(models.Page):

	name = djangomodels.CharField(max_length=63)

# Panel definitions for ToolPage
ToolPage.content_panels = models.Page.content_panels + [

	FieldPanel('name'),
	InlinePanel('modules', label='Modules')
]

@register_snippet
class Module(djangomodels.Model):

	page = ParentalKey('home.ToolPage', related_name='modules', null=True, blank=True)
	name = djangomodels.CharField(max_length=50)

Module.panels = [
	
	FieldPanel('name'),
]

class HomePage(models.Page):
    pass
