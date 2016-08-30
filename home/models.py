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

#from .forms import TaskCreationForm

USER_ROLE_CHOICES = (
	(1, 'HW'),
	(2, 'Process')
)

TASK_PRIORITY_CHOICES = (
	(0, 'None'),
	(1, 'HIGH'),
	(2, 'MEDIUM'),
	(3, 'LOW')
)

TASK_STATUS_CHOICES = (
	(0, 'To Do'),
	(1, 'In Progress'),
	(2, 'Done'),
	(3, 'Proposed'),
	(4, 'rejected')
)

REQUEST_CHOICES = (
	(0, 'Requested'),
	(1, 'Accepted'),
	(2, 'Rejected'),
	(3, 'Planned')
)

@register_snippet
class DashboardUser(djangomodels.Model):

	user = djangomodels.OneToOneField(settings.AUTH_USER_MODEL)
	group = djangomodels.CharField(max_length=63, null=True)
	company = djangomodels.CharField(max_length=63, null=True)
	role = djangomodels.IntegerField(default=1, choices=USER_ROLE_CHOICES)

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


@register_snippet
class Request(djangomodels.Model):

	name = djangomodels.CharField(max_length=127)
	description = djangomodels.TextField()
	owner = djangomodels.ForeignKey('home.DashboardUser', null=True, blank=True)
	due_date = djangomodels.DateField(default=datetime.date.today)
	requisition_date = djangomodels.DateField(auto_now_add=True, null=True)
	status = djangomodels.ForeignKey('home.RequestStatus', default=0)
	tool = ParentalKey('home.ToolPage', related_name='requests', null=True, blank=True)

	class Meta:
		ordering = ['tool', 'owner']

	def __str__(self):
		return self.name


class RequestStatus(djangomodels.Model):

	rejection_reason = djangomodels.CharField(max_length=256)
	status = djangomodels.IntegerField(choices=REQUEST_CHOICES, default=0)
	last_update = djangomodels.DateField(default=datetime.date.today)

	def __str__(self):
		return self.status


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
	title = djangomodels.CharField(max_length=90)
	description = djangomodels.CharField(max_length=510)
	start_datetime = djangomodels.DateTimeField(blank=True, null=True)
	due_datetime = djangomodels.DateTimeField(blank=True, null=True)

	owner = djangomodels.ForeignKey('home.DashboardUser', blank=True, null=True, related_name='tasks')
	requisitioner = djangomodels.ForeignKey('home.DashboardUser', blank=True, null=True, related_name='requested_tasks')

	event = ParentalKey('home.EventPage', related_name='tasks', blank=True, null=True)
	module = djangomodels.ForeignKey('home.ToolModule', related_name='tasks', null=True, blank=True)

	priority = djangomodels.IntegerField(choices=TASK_PRIORITY_CHOICES, null=True, default=0)
	status = djangomodels.IntegerField(choices=TASK_STATUS_CHOICES, null=False, default=0)
	single = djangomodels.BooleanField(default=True)


	# Managers
	objects = djangomodels.Manager()
	loose_tasks = LooseTasksManager()

	# Forms
	#base_form_class = TaskCreationForm

	class Meta:
		pass

	def __str__(self):
		return self.title

	@property
	def bs_color(self):
		# case: Done
		if self.status == 2:
			return 'success'
		else:
			if self.priority == 0:
				return 'info'
			elif self.priority == 1:
				return 'danger'
			elif self.priority == 2:
				return 'warning'
			elif self.priority == 3:
				return 'primary'

Task.panels = [
	MultiFieldPanel([
		FieldRowPanel([
			FieldPanel('title', classname='col8'),
			FieldPanel('priority', classname='col4'),
			FieldPanel('description',classname='col12'),
			]
		),
		FieldRowPanel([
			FieldPanel('module', classname='col6'),
			FieldPanel('owner', classname='col6')
			]
		), 
		FieldRowPanel([
			FieldPanel('start_datetime'),
			FieldPanel('due_datetime')
			]
		)], heading='Task information'
	),
]

class EventPage(models.Page):
	'''
	Een event kan een groot onderhoud, escalatie, installatie, VWV of andere zijn. 
	Een event wordt opgebouwd uit taken, en is gelinkt aan een module (dus Main module in geval van tool)
	'''
	name = djangomodels.CharField('title', max_length=63)
	description = djangomodels.TextField(max_length=510, blank=True, null=True)

	start_date = djangomodels.DateTimeField(blank=True, null=True)
	end_date = djangomodels.DateTimeField(blank=True, null=True)

	responsible = djangomodels.ForeignKey(settings.AUTH_USER_MODEL, related_name='events', blank=True, null=True)

	module = djangomodels.ForeignKey('home.ToolModule', related_name='events', null=True, blank=True)

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

		return super(EventPage, self).save(*args, **kwargs)

	@property
	def task_count_distinct_owner(self):

		return Task.objects.all().filter(event=self).values('owner').distinct().count()

	@property
	def todo_tasks(self):
		return Task.objects.all().filter(event=self).filter(status=0)

	@property
	def inprogress_tasks(self):
		return Task.objects.all().filter(event=self).filter(status=1)

	@property
	def done_tasks(self):
		return Task.objects.all().filter(event=self).filter(status=2)
	

	
# Panel definitions for ToolPage
EventPage.content_panels =  [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('module', classname='col6')
				]
			),
			FieldRowPanel([
					FieldPanel('description', classname='col12'),
				]
			),
		],
		heading='Event information'
	),
	InlinePanel('tasks', label='tasks', help_text='Every event needs at least 1 task to be functional'),
]

EventPage.promote_panels = [
]


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

	    loose_tasks = Task.objects.all().filter(module__tool=self).filter(event=None)
	    return loose_tasks
	

	@route(r'^tasks/$')
	def tasks(self, request):

		template = 'task/tasks.html'

		context = {}
		context['loose_tasks'] = Task.loose_tasks.all()

		return TemplateResponse(request, template=template, context=context)


	@property
	def requested_requests(self):
		return Request.objects.all().filter(tool=self).filter(status=0)

	@property
	def rejected_requests(self):
		return Request.objects.all().filter(tool=self).filter(status=1)

	@property
	def accepted_requests(self):
		return Request.objects.all().filter(tool=self).filter(status=2)

	@property
	def planned_requests(self):
		return Request.objects.all().filter(tool=self).filter(status=2)


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
		ordering = ['tool', 'name', ]

	def __str__(self):

		return '%s: module %s' % (self.tool, self.name)

	def save(self, *args, **kwargs):

		return super(ToolModule, self).save(*args, **kwargs)

ToolModule.panels = [
	
	FieldPanel('name'),
	FieldPanel('is_main')
]


class HomePage(models.Page):
    pass
