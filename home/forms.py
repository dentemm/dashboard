from django import forms

from .widgets import CustomDateTimeInput
from .models import Task

class TaskForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['start_datetime'].widget = CustomDateTimeInput()
		self.fields['due_datetime'].widget = CustomDateTimeInput()

	class Meta:
		model = Task
		fields = ['title', 'description', 'start_datetime', 'due_datetime', 'owner', 'priority', ]
