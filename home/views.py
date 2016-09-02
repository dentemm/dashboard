from django.views.generic import TemplateView, CreateView

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Task, EventPage, ToolModule, ToolPage, Request
from .forms import TaskForm, RequestForm

#
#
# TASK VIEWS
#
#
class TaskView(TemplateView):

	template_name = 'task/tasks.html'

class TaskModalView(TemplateView):
	'''
	Dit view wordt gebruikt om een modal window te tonen waar je de details van een Task object kan raadplegen
	'''

	template_name = 'task/modals/taskmodal.html'

	def get_context_data(self, **kwargs):

		ctx = super(TaskModalView, self).get_context_data(**kwargs)

		task_id = self.kwargs['id']

		#print('task: %s' % task_id)

		ctx['task'] = Task.objects.get(id=task_id)

		return ctx

class AddTaskModalView(CreateView):
	'''
	Dit modal view voegt een extra Task object toe aan een Event, of een losse Task aan een Tool
	'''

	template_name = 'task/modals/addtaskmodal.html'
	model = Task
	form_class = TaskForm

	event_id = None
	tool_id = None
	
	def dispatch(self, request, *args, **kwargs):

		# Kijk na of de kwargs een event_id of tool_id bevatten
		event_id = kwargs.get('event_id', 'empty')
		tool_id = kwargs.get('tool_id', 'empty')

		if event_id != 'empty':
			self.event_id = int(event_id)

		if tool_id != 'empty':
			self.tool_id = int(tool_id)

		return super(AddTaskModalView, self).dispatch(request, *args, **kwargs)


	def get(self, request, *args, **kwargs):		
		return super(AddTaskModalView, self).get(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		#print('event: %s' % event_id)
		#print('tool: %s' % tool_id)

		return super(AddTaskModalView, self).post(request, *args, **kwargs)

	def get_form(self, form_class=None):

		form = super(AddTaskModalView, self).get_form(form_class)

		if self.event_id != None:
			form.instance.event = EventPage.objects.get(id=self.event_id)
			form.instance.single = False 

		if self.tool_id != None:
			tool = ToolPage.objects.get(id=self.tool_id)
			module = ToolModule.objects.get(tool=tool, is_main=True)

			form.instance.module = module
			form.instance.single = True

		return form

	def get_form_kwargs(self):

		kwargs = super(AddTaskModalView, self).get_form_kwargs()

		print('---form kwargs: %s' % kwargs)
		print(self.tool_id)
		print(self.event_id)

		return kwargs

	def get_context_data(self, **kwargs):

		ctx = super(AddTaskModalView, self).get_context_data(**kwargs)

		event_id = self.kwargs.get('event_id', 'empty')
		tool_id = self.kwargs.get('tool_id', 'empty')

		if event_id != 'empty':
			ctx['tool'] = EventPage.objects.get(id=event_id)
			ctx['post_url'] = '/tasks/new/event/%s/' % event_id

		if tool_id != 'empty':
			ctx['tool'] = ToolPage.objects.get(id=tool_id)
			ctx['post_url'] = 'tasks/new/tool/%s/' % tool_id

		
		print(' ----- url: %s' % ctx['post_url']) 

		return ctx

#
#
# REQUEST VIEWS
#
#
class AddRequestModalView(CreateView):
	'''
	Dit modal view voegt een extra Request object toe aan een Tool
	'''

	template_name = 'request/modals/addrequestmodal.html'
	model = Request
	form_class = RequestForm	

	def dispatch(self, request, *args, **kwargs):

		# Kijk na of de kwargs een event_id of tool_id bevatten
		tool_id = kwargs.get('tool_id', 'empty')

		if tool_id != 'empty':
			self.tool_id = int(tool_id)

		return super(AddRequestModalView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')
		return super(AddRequestModalView, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(AddRequestModalView, self).get_context_data(**kwargs)

		if self.tool_id != 'empty':
			ctx['tool'] = ToolPage.objects.get(id=self.tool_id)
			ctx['post_url'] = '/requests/new/tool/%s/' % self.tool_id

		return ctx

	def get_form(self, form_class=None):

		form = super(AddRequestModalView, self).get_form(form_class)

		if self.tool_id != None:
			tool = ToolPage.objects.get(id=self.tool_id)
			form.instance.tool = tool

		return form

#
#
# API VIEWS
#
#
class TasksForEventApiView(APIView):
	'''
	Dit view retourneert een JSON response van alle taken voor een bepaald event. 
	Deze taken worden gebruikt door FullCalendar
	'''

	def dispatch(self, request, *args, **kwargs):

		self.event_id = kwargs.pop('event_id', None)

		return super(TasksForEventApiView, self).dispatch(request, *args, **kwargs)


	def get(self, request, format=None):

		# FullCalandar verwacht een events JSON list 

		tasks = Task.objects.filter(event__pk=self.event_id)

		events = []

		for task in tasks:

			color = ''

			if task.status == 2:
				color = '#1bc98e'

			else:
				if task.priority == 1:
					color = '#e64759' 

				elif task.priority == 2:
					color = '#FF9017'

				elif task.priority == 3:
					color = '#1ca8dd'

				else:
					color = '#9f86ff'


			events.append({
				'id': task.pk, 'resourceId': task.owner.pk, 'start': task.start_datetime, 'end': task.due_datetime, 'title': task.title, 'color': color
			})

		return Response(events)
		
class ResourcesForEventApiView(APIView):
	'''
	Dit view retourneert een JSON response van alle resources (= imec medewerkers) voor een bepaald event.
	Deze resources worden gebruikt door FullCalendar
	'''

	def dispatch(self, request, *args, **kwargs):

		self.event_id = kwargs.pop('event_id', None)

		return super(ResourcesForEventApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tasks = Task.objects.filter(event__pk=self.event_id)

		resources = []

		for task in tasks:
			resources.append({
				'id': task.owner.user.id, 'title': task.owner.user.username
			})

		return Response(resources)

class ActivitiesForToolApiView(APIView):

	def dispatch(self, request, *args, **kwargs):

		self.tool_id = kwargs.pop('tool_id', None)

		print('tool id: %s' % self.tool_id)

		return super(ActivitiesForToolApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tool_tasks = Task.objects.filter(module__tool__pk=self.tool_id)
		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		events = []

		for task in tool_tasks:

			color = ''

			if task.status == 2:
				color = '#1bc98e'

			else:
				if task.priority == 1:
					color = '#e64759' 

				elif task.priority == 2:
					color = '#FF9017'

				elif task.priority == 3:
					color = '#1ca8dd'

				else:
					color = '#9f86ff'


			events.append({
				'id': task.pk, 'resourceId': task.owner.pk, 'start': task.start_datetime, 'end': task.due_datetime, 'title': task.title, 'color': color
			})

		return Response(events)

class ResourcesForToolApiView(APIView):

	def dispatch(self, request, *args, **kwargs):

		self.tool_id = kwargs.pop('tool_id', None)

		print('tool id: %s' % self.tool_id)

		return super(ResourcesForToolApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tool_tasks = Task.objects.filter(module__tool__pk=self.tool_id)
		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		resources = []

		for task in tool_tasks:
			resources.append({
				'id': task.owner.user.id, 'title': task.owner.user.username
			})

		return Response(resources)
