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

		tasks = Task.objects.filter(event__pk=self.event_id)

		events = []

		for task in tasks:

			print('tijdstip: %s' % task.start_datetime)

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
				'id': task.owner.id, 'title': task.owner.username
			})

		'''resources = [
          	{ 'id': '1', 'title': 'Wim' },
          	{ 'id': '1', 'title': 'Wim' },
          	{ 'id': '2', 'title': 'Tim' },
          	{ 'id': '3', 'title': 'Damiaan' },
          	{ 'id': '4', 'title': 'Pedro' },
          	{ 'id': '4', 'title': 'Ko' },
          	{ 'id': '6', 'title': 'Teblick' },
          	{ 'id': '7', 'title': 'Hookup' },
          	{ 'id': '8', 'title': 'Top ingenieur' },
          	{ 'id': '8', 'title': 'Top ingenieur' },
		]'''

		return Response(resources)
