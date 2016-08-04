from __future__ import absolute_import, unicode_literals

from django.db import models as djangomodels
from django.conf import settings

from wagtail.wagtailcore import models
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey

@register_snippet
class Fab(djangomodels.Model):
	'''
	Deze klasse beschrijft een FAB
	'''
	name = djangomodels.CharField(max_length=8)

	def __str__(self):
		return self.name


@register_snippet
class Utility(djangomodels.Model):
	'''
	Deze klasse beschrijft een utility
	'''

	name = djangomodels.CharField(max_length=31)
	description = djangomodels.TextField()
	fab = djangomodels.ForeignKey(Fab, related_name='facilities', null=True)

	status = djangomodels.OneToOneField('home.UtilityStatus', null=True, blank=True)

	class Meta:
		verbose_name_plural = 'utilities'

	def __str__(self):
		return self.name

Utility.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('fab', classname='col6'),
					FieldPanel('description', classname='col12')
				]
			),
		],
		heading='Utilities'
	),
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('status', classname='col6'),
				]
			),
		],
		heading='Status'
	)
]


@register_snippet
class UtilityStatus(djangomodels.Model):
	'''
	Deze klasse wordt gebruikt om de status van een bepaalde utility aan te geven
	'''

	name = djangomodels.CharField(max_length=63)
	description = djangomodels.TextField()

	class Meta:
		verbose_name_plural = 'utility status'

	def __str__(self):
		return self.name

UtilityStatus.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('description', classname='col12')
				]
			),
		],
		heading='Utility datas'
	)
]


class ToolUtilityStatusValue(djangomodels.Model):
	'''
	Join model tussen ToolPage en UtilityStatus klassen
	'''

	tool = ParentalKey('home.ToolPage', related_name='utilities', null=True, blank=True)
	status = djangomodels.ForeignKey(UtilityStatus, related_name='tools', null=True, blank=True)



@register_snippet
class Task(djangomodels.Model):
	'''

	'''

	title = djangomodels.CharField(max_length=63)
	description = djangomodels.CharField(max_length=510)
	due_datetime = djangomodels.DateTimeField(blank=False, null=True)
	completed = djangomodels.BooleanField(default=False)

	owner = djangomodels.ForeignKey(settings.AUTH_USER_MODEL)
	tool = djangomodels.ForeignKey('home.ToolPage', related_name='tasks', null=True)

	page = ParentalKey('home.SafeWorkingPermit', related_name='tasks')

	class Meta:
		pass

Task.panels = [
	
	FieldPanel('title'),
	FieldPanel('description'),
	FieldPanel('tool'),
]



class SafeWorkingPermit(models.Page):

	vwv_owner = djangomodels.ForeignKey('home.DashboardUser')
	vwv_title = djangomodels.CharField(max_length=63)
	description = djangomodels.CharField(max_length=510)
	start_date = djangomodels.DateTimeField(null=True, blank=False)
	end_date = djangomodels.DateTimeField(null=True, blank=False)
	tool = djangomodels.ForeignKey('home.ToolPage', null=True, blank=True, related_name='+')

	class Meta:
		pass


	def tasks_for_tool_completed(self, tool):
		'''
		Retourneer True als alle taken voor een gegeven tool afgewerkt zijn. Mogelijk maken we hier beter 
		(ook) een template tag van
		'''

		for task in tool.tasks:

			if task.completed == False:
				return False

		return True


# Panel definitions for SafeWorkingPermit page
SafeWorkingPermit.content_panels = models.Page.content_panels + [

	FieldPanel('vwv_title'),
	FieldPanel('vwv_owner'),
	FieldPanel('start_date'),
	InlinePanel('tasks', label='Tasks'),
	InlinePanel('involved_parties', label='Betrokken Partijen'),
	PageChooserPanel('tool'),
	InlinePanel('tools', label='tools')
]

#@register_snippet
class DashboardUser(djangomodels.Model):

	user = djangomodels.OneToOneField(settings.AUTH_USER_MODEL)
	group = djangomodels.CharField(max_length=63, null=True)
	company = djangomodels.CharField(max_length=63, null=True)

	def __str__(self):
		return 'custom user model'

DashboardUser.panels = [
	FieldPanel('user'),
]

class SafeworkingPermitUser(djangomodels.Model):

	user = djangomodels.ForeignKey('home.DashboardUser')
	page = ParentalKey('home.SafeWorkingPermit', related_name='involved_parties')
	role = djangomodels.CharField(max_length=8) # Welke rol heeft deze gebruiker voor een gegeven Veilig Werk Vergunning?

	
class SafeworkingPermitTool(djangomodels.Model):

	page = ParentalKey('home.SafeWorkingPermit', related_name='tools')
	tool = djangomodels.ForeignKey('home.ToolPage')



class ToolPage(models.Page):
	'''
	Mogelijk moet ik hier een standaar django model van maken, de meerwaarde is op dit moment vrij klein
	'''

	name = djangomodels.CharField(max_length=63)
	tool_number = djangomodels.PositiveIntegerField(null=True, blank=True)
	vwv = djangomodels.ForeignKey('home.SafeWorkingPermit', null=True, blank=True, related_name='toolen')


# Panel definitions for ToolPage
ToolPage.content_panels = models.Page.content_panels + [

	FieldPanel('name'),
	InlinePanel('modules', label='Modules')
]

class FacilityStatusPage(models.Page):
	'''
	'''

	template = 'home/facility_status.html'

	pass 

@register_snippet
class Module(djangomodels.Model):
	'''
	Een module van een Tool object
	'''

	page = ParentalKey('home.ToolPage', related_name='modules', null=True, blank=True)
	name = djangomodels.CharField(max_length=50)

Module.panels = [
	
	FieldPanel('name'),
]

class HomePage(models.Page):
    pass
