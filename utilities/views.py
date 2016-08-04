from datetime import datetime

from django.shortcuts import render
from django import views

from home.models import Fab, Utility, UtilityStatus

# Create your views here.


class OverviewView(views.generic.TemplateView):

	template_name = 'utilities/utilities.html'

	def get_context_data(self, **kwargs):

		ctx = super(OverviewView, self).get_context_data(**kwargs)
		ctx['fab'] = self.fab

		utilities = self._get_utitilies(self.fab)
		ctx['utilities'] = utilities
		ctx['status'] = self.status



		ctx['now'] = datetime.now()

		return ctx


	def get(self, request, *args, **kwargs):

		self.fab = request.GET.get('fab', 'fab1')
		utility = request.GET.get('utility', 'diw')
		toggle = request.GET.get('toggle', 'toggle')

		self._toggle_utility_status(utility)

		return super(OverviewView, self).get(request, *args, **kwargs)


	def _get_utitilies(self, fab):

		try: 
			fab = Fab.objects.get(name__iexact=self.fab)

		except:
			print('ERROR')
			return None

		utilities = fab.facilities.all()

		#print('fab: %s ' % fab)
		#print('facilities %s' % utilities)

		return utilities

	def _toggle_utility_status(self, utility):

		util = Utility.objects.get(name__iexact=utility)

		if util.status.name == 'green':
			status = UtilityStatus.objects.get(name='red')

		elif util.status.name == 'red':
			status = UtilityStatus.objects.get(name='green')

		else:
			status = UtilityStatus.objects.get(name='red')

		self.status = status.name

		print('status: %s' % self.status)

		util.status = status
		util.save()


