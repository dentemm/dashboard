from django.core.management.base import BaseCommand, CommandError

from datetime import datetime

from home.models import EventPage, Task

class Command(BaseCommand):

	help = 'Adds end and start date for all events'

	def handle(self, *args, **options):

		for event in EventPage.objects.all():

			start = datetime(3000, 1, 1)
			end = datetime(2000, 1, 1)

			for task in Task.objects.filter(event=event):

				if task.start_datetime < start:
					start = task.start_datetime

				if task.due_datetime > end:
					end = task.due_datetime

			event.start_date = start
			event.end_date = end
			event.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))

