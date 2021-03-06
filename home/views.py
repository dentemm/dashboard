from datetime import timedelta, datetime, time

from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.http import HttpResponse
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Task, EventPage, ToolModule, ToolPage, Request
from .forms import TaskForm, TaskUpdateForm, RequestForm, RequestUpdateForm, PlanRequestUpdateForm, AcceptRequestUpdateForm
from .forms import EventForm


#
#
# HELPER METHODES
#
#
def get_color_for_task(task):
	'''
	Retourneer een kleur voor een gegeven taak
	'''

	if task.status == 2:
		return '#1bc98e'

	else:
		if task.priority == 1:
			return '#e64759' 

		elif task.priority == 2:
			return '#FF9017'

		elif task.priority == 3:
			return '#1ca8dd'

		else:
			return '#1ca8dd'

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

	template_name = 'task/modals/task_event_modal.html'

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

		#print('---form kwargs: %s' % kwargs)
		#print(self.tool_id)
		#print(self.event_id)

		return kwargs

	def get_context_data(self, **kwargs):

		ctx = super(AddTaskModalView, self).get_context_data(**kwargs)

		event_id = self.kwargs.get('event_id', 'empty')
		tool_id = self.kwargs.get('tool_id', 'empty')

		if event_id != 'empty':
			ctx['tool'] = EventPage.objects.get(id=event_id)
			ctx['post_url'] = reverse('add-task-for-event', kwargs={'event_id': event_id})

		if tool_id != 'empty':
			ctx['tool'] = ToolPage.objects.get(id=tool_id)
			ctx['post_url'] = reverse('add-task-for-tool', kwargs={'tool_id': tool_id})

		return ctx

class CalendarEventModalViewEvent(TemplateView):

	template_name = 'tool/modals/task_event_modal.html'

	def get(self, request, *args, **kwargs):

		return super(CalendarEventModalViewEvent, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(CalendarEventModalViewEvent, self).get_context_data(**kwargs)

		event_slug = self.kwargs.get('event_slug')

		event = EventPage.objects.get(slug=event_slug)

		ctx['event'] = event

		return ctx

class CalendarEventModalViewTask(UpdateView):

	template_name = 'task/modals/updatetaskmodal.html'
	model = Task
	form_class = TaskUpdateForm

	def post(self, request, *args, **kwargs):
		self.success_url = request.META.get('HTTP_REFERER')
		return super(CalendarEventModalViewTask, self).post(request, *args, **kwargs)


	def get_context_data(self, **kwargs):

		ctx = super(CalendarEventModalViewTask, self).get_context_data(**kwargs)

		tool_id = self.kwargs.get('pk', 'empty')

		if tool_id != 'empty':
			ctx['post_url'] = reverse('tool-calendar-modal-task', kwargs={'pk': tool_id})

		return ctx

class UpdateTasksForEventView(View):

	def _allowed_methods(self):

		return ('POST', 'PUT', 'GET')

	def post(self, request, *args, **kwargs):

		todo_tasks = request.POST.getlist('todo[]')
		done_tasks = request.POST.getlist('inprogress[]')
		inprogress_tasks = request.POST.getlist('done[]')

		event_id = int(kwargs['event_id'])

		page = EventPage.objects.get(pk=event_id)

		if len(todo_tasks) > 0:
			self.update_tasks_with_status(todo_tasks, 0)

		if len(done_tasks) > 0:
			self.update_tasks_with_status(done_tasks, 1)

		if len(inprogress_tasks) > 0:
			self.update_tasks_with_status(inprogress_tasks, 2)

		return HttpResponse()


	def update_tasks_with_status(self, tasks, status):

		for item in tasks:

			task = Task.objects.get(pk=item)
			task.status = status
			task.save()

class UpdateTasksForToolView(View):

	def _allowed_methods(self):

		return ('POST', 'PUT', 'GET')

	def post(self, request, *args, **kwargs):

		todo_tasks = request.POST.getlist('todo[]')
		done_tasks = request.POST.getlist('inprogress[]')
		inprogress_tasks = request.POST.getlist('done[]')

		tool_id = int(kwargs['tool_id'])

		page = ToolPage.objects.get(pk=tool_id)

		if len(todo_tasks) > 0:
			self.update_tasks_with_status(todo_tasks, 0)

		if len(done_tasks) > 0:
			self.update_tasks_with_status(done_tasks, 1)

		if len(inprogress_tasks) > 0:
			self.update_tasks_with_status(inprogress_tasks, 2)

		return HttpResponse()


	def update_tasks_with_status(self, tasks, status):

		for item in tasks:

			task = Task.objects.get(pk=item)
			task.status = status
			task.save()

#
#
# EVENT VIEWS
#
#
class AddEventModalView(CreateView):

	template_name = 'event/modals/addeventmodal.html'
	model = EventPage
	form_class = EventForm

	tool_id = None
	
	def dispatch(self, request, *args, **kwargs):

		# Kijk na of de kwargs een event_id of tool_id bevatten
		tool_id = kwargs.get('tool_id', 'empty')

		if tool_id != 'empty':
			self.tool_id = int(tool_id)

		return super(AddEventModalView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')
		return super(AddEventModalView, self).post(request, *args, **kwargs)

	def get_form(self, form_class=None):

		form = super(AddEventModalView, self).get_form(form_class)
		tool = ToolPage.objects.get(id=self.tool_id)
		form.instance.module = ToolModule.objects.get(tool=tool, is_main=True)
		form.instance.depth = 4

		highest = 0
		digits = 0

		for event in EventPage.objects.all():

			path_last_part = event.path[-4:]

			if(int(path_last_part) > highest):
				highest = int(path_last_part)

		highest = highest + 1

		digits = len(str(highest))

		if digits == 1:
			last_part = '000%s' % highest

		elif digits == 2:
			last_part = '00%s' % highest

		elif digits == 3:
			last_part = '0%s' % highest

		else:
			last_part = '%s' % highest

		path = '000100010001%s' % last_part

		form.instance.path = path

		return form

	def get_context_data(self, **kwargs):

		ctx = super(AddEventModalView, self).get_context_data(**kwargs)

		tool_id = self.kwargs.get('tool_id', 'empty')


		if tool_id != 'empty':
			ctx['tool'] = ToolPage.objects.get(id=tool_id)
			ctx['post_url'] = reverse('add-event-for-tool', kwargs={'tool_id': tool_id})

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
			ctx['post_url'] = reverse('add-request-for-tool', kwargs={'tool_id': self.tool_id})

		return ctx

	def get_form(self, form_class=None):

		form = super(AddRequestModalView, self).get_form(form_class)

		if self.tool_id != None:
			tool = ToolPage.objects.get(id=self.tool_id)
			form.instance.tool = tool

		return form

class RequestUpdateView(UpdateView):

	template_name = 'request/partials/update_request.html'
	model = Request
	form_class = RequestUpdateForm	

	def _allowed_methods(self):

		return ('POST', 'PUT', 'GET')

	def dispatch(self, request, *args, **kwargs):

		self.pk = kwargs['pk']

		return super(RequestUpdateView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):

		self.status = int(request.GET.get('status', 0))
		print('get status: %s' % self.status)

		return super(RequestUpdateView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		print('post')

		self.status = int(request.POST.get('status', 0))
		self.success_url = request.META.get('HTTP_REFERER')

		print('post status: %s' % self.status)

		return super(RequestUpdateView, self).post(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):

		ctx = super(RequestUpdateView, self).get_context_data(*args, **kwargs)
		request = Request.objects.get(pk=self.pk)
		ctx['request'] = request
		ctx['post_url'] = reverse('update-request', kwargs={'pk': self.pk})

		return ctx

	def get_form(self, form_class=None):

		form = super(RequestUpdateView, self).get_form(form_class)

		form.instance.status = self.status

		return form

	def get_form_kwargs(self):

		form_kwargs = super(RequestUpdateView, self).get_form_kwargs()

		return form_kwargs


	def get_extra_form_kwargs_for_status(self, status):

		data = {'extra': 'test'}

		return data

class RejectRequestUpdateView(UpdateView):

	model = Request
	fields = ['rejection_reason', ]
	template_name = 'request/modals/rejectrequestmodal.html'

	def dispatch(self, *args, **kwargs):

		self.pk = kwargs['pk']

		return super(RejectRequestUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):

		ctx = super(RejectRequestUpdateView, self).get_context_data(*args, **kwargs)
		request = Request.objects.get(pk=self.pk)
		ctx['request'] = request
		ctx['post_url'] = reverse('update-reject-request', kwargs={'pk': self.pk})

		return ctx

	def get_form(self, form_class=None):

		form = super(RejectRequestUpdateView, self).get_form(form_class)
		form.instance.status = 1	#REJECT!

		return form

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(RejectRequestUpdateView, self).post(request, *args, **kwargs)

class AcceptRequestUpdateView(UpdateView):

	model = Request
	form_class = AcceptRequestUpdateForm
	template_name = 'request/partials/update_request.html'

	def dispatch(self, *args, **kwargs):

		self.pk = kwargs['pk']
		return super(AcceptRequestUpdateView, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(AcceptRequestUpdateView, self).post(request, *args, **kwargs)

	def get_context_date(self, *args, **kwargs):

		ctx = super(AcceptRequestUpdateView, self).get_context_data(*args, **kwargs)
		request = Request.objects.get(pk=self.pk)
		ctx['request'] = request
		ctx['post_url'] = reverse('update-accept-request', kwargs={'pk': self.pk})

		return ctx

	def get_form(self, form_class=None):
		form = super(AcceptRequestUpdateView, self).get_form(form_class)
		form.instance.status = 2

		return form

class PlanRequestUpdateView(UpdateView):

	model = Request
	form_class = PlanRequestUpdateForm
	template_name = 'request/partials/update_request.html'

	def dispatch(self, *args, **kwargs):

		self.pk = kwargs['pk']

		return super(PlanRequestUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):

		ctx = super(PlanRequestUpdateView, self).get_context_data(*args, **kwargs)
		request = Request.objects.get(pk=self.pk)
		ctx['request'] = request
		ctx['post_url'] = reverse('update-plan-request', kwargs={'pk': self.pk})

		return ctx

	def get_form(self, form_class=None):

		form = super(PlanRequestUpdateView, self).get_form(form_class)
		form.instance.status = 3	#PLAN!

		return form

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(PlanRequestUpdateView, self).post(request, *args, **kwargs)

	def form_valid(self, form):

		self.object = form.save()

		#print('due datetime: %s' % due_datetime.time)

		start_datetime = datetime.combine(self.object.planned_date, time(6))
		due_datetime = datetime.combine(self.object.planned_date, time(22))	

		
		task = Task(description=self.object.description, title=self.object.name,
				module=self.object.tool.modules.all().filter(is_main=True).first(), owner=self.object.task_owner, 
				start_datetime=start_datetime, due_datetime=due_datetime
				)

		task.save()

		return super(PlanRequestUpdateView, self).form_valid(form)
	


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

			color = get_color_for_task(task)

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

		tool = ToolPage.objects.get(pk=self.tool_id)
		tool_tasks = tool.loose_tasks

		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		events = []

		for task in tool_tasks:

			color = get_color_for_task(task)

			events.append({
				'id': task.pk, 'resourceId': task.owner.pk, 'start': task.start_datetime, 'end': task.due_datetime, 'title': task.title, 'color': color
			})

		for event in tool_events:

			color = '#9f86ff'

			events.append({
				'id': event.slug, 'resourceId': event.responsible.pk, 'start': event.start_date, 'end': event.end_date, 'title': event.name, 'color': color
			})

		return Response(events)

class ResourcesForToolApiView(APIView):

	def dispatch(self, request, *args, **kwargs):

		self.tool_id = kwargs.pop('tool_id', None)

		print('tool id: %s' % self.tool_id)

		return super(ResourcesForToolApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tool = ToolPage.objects.get(pk=self.tool_id)
		tool_tasks = tool.loose_tasks

		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		resources = []

		for task in tool_tasks:
			resources.append({
				'id': task.owner.user.id, 'title': task.owner.user.username
			})

		for event in tool_events:

			resources.append({
				'id': event.responsible.pk, 'title': event.responsible.username
			})

		return Response(resources)
