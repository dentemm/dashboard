from django.views.generic import TemplateView

class TaskView(TemplateView):

	template_name = 'task/tasks.html'
