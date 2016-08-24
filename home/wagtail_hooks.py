from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.wagtailcore import hooks



@hooks.register('insert_global_admin_css')
def global_admin_css():
	'''
	Deze wagtail hook wordt gebruikt om enkele styling aanpassingen door te voeren aan de admin interface
	'''

	print('---------- editor css')

	return format_html(
		'<link rel="stylesheet" href="{}">',
		static('css/wagtailoverrides.css')
	)	


