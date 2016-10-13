from django import forms

from .widgets import CustomDateTimeInput, CustomDateInput
from .models import Task, Request, EventPage

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

class EventForm(forms.ModelForm):

	class Meta:
		model = EventPage
		fields = ['name', 'description', 'responsible', 'module']


class RequestForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):

		super(RequestForm, self).__init__(*args, **kwargs)
		self.fields['due_date'].widget = CustomDateInput()

	class Meta:
		model = Request
		fields = ['name', 'description', 'owner', 'due_date', 'importance']

class RequestUpdateForm(forms.ModelForm):
	'''
	Test om request forms te refactoren
	'''

	def __init__(self, *args, **kwargs):

		##extra_fields = kwargs.pop('extra')
		super(RequestUpdateForm, self).__init__(*args, **kwargs)
		self.fields['status'].widget = forms.HiddenInput()


	class Meta:
		model = Request
		fields = ['status', ]

class RejectRequestUpdateForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ['rejection_reason', ]

class AcceptRequestUpdateForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ['task_owner', ]

class PlanRequestUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(PlanRequestUpdateForm, self).__init__(*args, **kwargs)
		self.fields['planned_date'].widget = CustomDateInput()

	class Meta:
		model = Request
		fields = ['planned_date', 'task_owner']



class RejectAcceptUpdateForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ['status', ]