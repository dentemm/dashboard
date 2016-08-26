from django import forms

from .widgets import CustomDateTimeInput
from .models import Task

class TaskForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		print 

		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['start_datetime'].widget = CustomDateTimeInput()

		print('succes')

	class Meta:
		model = Task
		fields = '__all__'
