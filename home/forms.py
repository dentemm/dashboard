from django import forms

from .widgets import CustomDateTimeInput, CustomDateInput
from .models import Task, Request

class TaskForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['start_datetime'].widget = CustomDateTimeInput()
		self.fields['due_datetime'].widget = CustomDateTimeInput()

	class Meta:
		model = Task
		fields = ['title', 'description', 'start_datetime', 'due_datetime', 'owner', 'priority', ]

class TaskUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(TaskUpdateForm, self).__init__(*args, **kwargs)
		self.fields['start_datetime'].widget = CustomDateTimeInput()
		self.fields['due_datetime'].widget = CustomDateTimeInput()

	class Meta:
		model = Task
		fields = ['owner', 'priority', 'start_datetime', 'due_datetime', 'status' ]

class RequestForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):

		super(RequestForm, self).__init__(*args, **kwargs)
		self.fields['due_date'].widget = CustomDateInput()

	class Meta:
		model = Request
		fields = ['name', 'description', 'owner', 'due_date', 'importance']
