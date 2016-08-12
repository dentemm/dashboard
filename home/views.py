from django.views.generic import TemplateView

from .models import Task

class TaskView(TemplateView):

	template_name = 'task/tasks.html'

class TaskModalView(TemplateView):

	template_name = 'task/modals/taskmodal.html'

	def get_context_data(self, **kwargs):

		ctx = super(TaskModalView, self).get_context_data(**kwargs)

		task_id = self.kwargs['id']

		print('task: %s' % task_id)

		ctx['task'] = Task.objects.get(id=task_id)

		print('jeej %s' % Task.objects.get(id=task_id))

		return ctx

