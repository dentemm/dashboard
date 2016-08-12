from __future__ import absolute_import, unicode_literals

import datetime

from django.db import models as djangomodels
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.template.response import TemplateResponse

from wagtail.wagtailcore import models
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailadmin.forms import WagtailAdminPageForm
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import PageManager


from modelcluster.fields import ParentalKey

ROLE_CHOICES = (
	(1, 'HW'),
	(2, 'Process')
)

@register_snippet
class DashboardUser(djangomodels.Model):

	user = djangomodels.OneToOneField(settings.AUTH_USER_MODEL)
	group = djangomodels.CharField(max_length=63, null=True)
	company = djangomodels.CharField(max_length=63, null=True)
	role = djangomodels.IntegerField(default=1, choices=ROLE_CHOICES)

	def __str__(self):

		return self.user.username

DashboardUser.panels = [
	FieldPanel('user'),
	FieldPanel('role'),
]

class HWToolResponsibles(djangomodels.Model):

	responsible = djangomodels.ForeignKey('home.DashboardUser', limit_choices_to={'role':1})
	tool = ParentalKey('home.ToolPage', related_name='hw_responsibles')

	def __str__(self):
		return self.responsible.user.username

HWToolResponsibles.panels = [
	FieldPanel('responsible')
]

class ProcessToolResponsibles(djangomodels.Model):

	responsible = djangomodels.ForeignKey('home.DashboardUser', limit_choices_to={'role':2})
	tool = ParentalKey('home.ToolPage', related_name='process_responsibles')

	def __str__(self):
		return self.responsible.user.username

ProcessToolResponsibles.panels = [
	FieldPanel('responsible')
]

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
	Deze klasse beschrijft een utility. Dient later nog geimplementeerd te worden
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


class Priority(djangomodels.Model):
	'''

	'''

	name = djangomodels.CharField(max_length=28)
	priority = djangomodels.PositiveIntegerField(default=1)


class LooseTasksManager(djangomodels.Manager):

	def get_queryset(self):

		return super(LooseTasksManager, self).get_queryset().filter(event=None)

@register_snippet
class Task(djangomodels.Model):
	'''
	Een task kan een op zich staande taak zijn, ofwel een taak die gerelateerd is aan een event. 
	Een task wordt steeds gelinkt aan een module (dus Main module in geval van tool)
	'''

	title = djangomodels.CharField(max_length=63)
	description = djangomodels.CharField(max_length=510)
	due_datetime = djangomodels.DateTimeField(blank=False, null=True)
	completed = djangomodels.BooleanField(default=False)

	owner = djangomodels.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	event = djangomodels.ForeignKey('home.Event', blank=True, null=True)
	module = djangomodels.ForeignKey('home.ToolModule', related_name='tasks', null=True, blank=True)


	# Managers
	objects = djangomodels.Manager()
	loose_tasks = LooseTasksManager()

	class Meta:
		pass

	def __str__(self):
		return self.title


Task.panels = [
	
	FieldPanel('title'),
	FieldPanel('description'),
	FieldPanel('module'),
	FieldPanel('owner')
]

@register_snippet
class Event(models.Page):
	'''
	Een event kan een groot onderhoud, escalatie, installatie, VWV of andere zijn. 
	Een event wordt opgebouwd uit taken, en is gelinkt aan een module (dus Main module in geval van tool)
	'''
	name = djangomodels.CharField('title', max_length=63)
	description = djangomodels.CharField(max_length=510)

	start_date = djangomodels.DateTimeField(blank=False, null=True)
	end_date = djangomodels.DateTimeField(blank=False, null=True)

	responsible = djangomodels.ForeignKey(settings.AUTH_USER_MODEL, related_name='events')

	class Meta:
		pass 

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		'''
		Deze methode werd overschreven om de title en slug attributes van een Page model in te stellen.
		Title en slug wordt gemaakt op basis van de name van een Event
		'''

		# -- PAGE TITLE AND PAGE SLUG FUNCTIONALITY -- #
		if self.slug == "" and self.title == "":
			self.title = self.name
			self.slug = slugify(self.name)

		return super(ToolPage, self).save(*args, **kwargs)



class ToolPageForm(WagtailAdminPageForm):
	'''
	Custom WagtailAdminPageForm subklasse. Deze wordt gebruikt om extra field validation te integreren
	Staat hier omwille van circular import!
	'''

	def clean(self):

		print('clean')

		page = self.instance
		cleaned_data = super(ToolPageForm, self).clean()

		return cleaned_data

class ToolPage(RoutablePageMixin, models.Page):
	'''
	
	'''
	template = 'home/tool.html'

	name = djangomodels.CharField(max_length=63, unique=True)
	tool_number = djangomodels.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		'''
		Deze methode werd overschreven om de title en slug attributes van een Page model in te stellen.
		Title en slug wordt gemaakt op basis van de name van een Tool
		'''
		# -- PAGE TITLE AND PAGE SLUG FUNCTIONALITY -- #
		if self.slug == "" and self.title == "":
			self.title = self.name
			self.slug = slugify(self.name)

		return super(ToolPage, self).save(*args, **kwargs)

	@property
	def submodules(self):

		return self.modules.all().exclude(is_main=True)
	

	@property
	def loose_tasks(self):

	    loose_tasks = Task.objects.all().filter(module__tool=self)
	    return loose_tasks
	

	@route(r'^tasks/$')
	def tasks(self, request):

		template = 'task/tasks.html'

		context = {}
		context['loose_tasks'] = Task.loose_tasks.all()

		return TemplateResponse(request, template=template, context=context)

# Panel definitions for ToolPage
ToolPage.content_panels =  [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('tool_number', classname='col6'),
				]
			),
		],
		heading='Tool information'
	),
	InlinePanel('modules', label='Modules', help_text='Every tool needs at least 1 module, this will be the main module!'),
	InlinePanel('hw_responsibles', label='HW responsibles'),
	InlinePanel('process_responsibles', label='process_responsibles'),
]

ToolPage.promote_panels = [
]


class FacilityStatusPage(models.Page):
	'''
	'''

	template = 'home/facility_status.html'

	pass 

@register_snippet
class ToolModule(djangomodels.Model):
	'''
	Een module van een ToolPage object. Elk toestel heeft tenminste 1 module, en dat is dan de main_module
	'''

	tool = ParentalKey('home.ToolPage', related_name='modules', null=True, blank=True)
	name = djangomodels.CharField(max_length=50)
	is_main = djangomodels.BooleanField(default=False)

	class Meta:
		ordering = ['name', ]

	def __str__(self):

		return '%s: module %s' % (self.tool, self.name)

	def save(self, *args, **kwargs):

		print('saving new module')

		return super(ToolModule, self).save(*args, **kwargs)


ToolModule.panels = [
	
	FieldPanel('name'),
	FieldPanel('is_main')
]

class HomePage(models.Page):
    pass
