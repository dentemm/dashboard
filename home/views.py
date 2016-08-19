from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Task

class TaskView(TemplateView):

	template_name = 'task/tasks.html'

class TaskModalView(TemplateView):

	template_name = 'task/modals/taskmodal.html'

	def get_context_data(self, **kwargs):

		ctx = super(TaskModalView, self).get_context_data(**kwargs)

		task_id = self.kwargs['id']

		#print('task: %s' % task_id)

		ctx['task'] = Task.objects.get(id=task_id)

		#print('jeej %s' % Task.objects.get(id=task_id))

		return ctx


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
		#events = []

		tasks = Task.objects.filter(event__pk=self.event_id)

		print('tasks for event: %s' % tasks)

		events = [
	          { 'id': '1', 'resourceId': 'b', 'start': '2016-08-07T04:00:00', 'end': '2016-08-08T07:00:00', 'title': 'Owner name', 'color': '#1bc98e'},
	          { 'id': '2', 'resourceId': 'c', 'start': '2016-08-09T05:00:00', 'end': '2016-08-12T22:00:00', 'title': 'event 2', 'color': '#FF9017'  },
	          { 'id': '3', 'resourceId': 'h', 'start': '2016-08-08T05:00:00', 'end': '2016-08-15T22:00:00', 'title': 'event 3', 'color': '#1ca8dd' },
	          { 'id': '4', 'resourceId': 'e', 'start': '2016-08-10T03:00:00', 'end': '2016-08-11T08:00:00', 'title': 'event 4', 'color': '#e64759' },
	          { 'id': '5', 'resourceId': 'f', 'start': '2016-08-08T00:30:00', 'end': '2016-08-08T06:30:00', 'title': 'event 5', 'color': '#9f86ff' }
		]

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

		resources = [
          	{ 'id': 'a', 'title': 'Wim' },
          	{ 'id': 'b', 'title': 'Tim' },
          	{ 'id': 'c', 'title': 'Damiaan' },
          	{ 'id': 'e', 'title': 'Pedro' },
          	{ 'id': 'f', 'title': 'Ko' },
          	{ 'id': 'g', 'title': 'Teblick' },
          	{ 'id': 'h', 'title': 'Hookup' },
          	{ 'id': 'i', 'title': 'Top ingenieur' },
		]

		return Response(resources)
