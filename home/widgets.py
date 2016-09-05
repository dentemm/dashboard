from __future__ import absolute_import, unicode_literals

import json 

from django.forms import widgets
from django.utils.safestring import mark_safe

class CustomDateInput(widgets.DateInput):
    '''
    Custom widget dat gebruikt wordt voor DateFields.
    Dit widget maakt gebruik van de jquery plugin DateTimePicker
    '''
    def __init__(self, attrs=None, format='%Y-%m-%d'):
        super(CustomDateInput, self).__init__(attrs=attrs, format=format)

    def render(self, name, value, attrs=None):

        try:
            id_ = attrs['id']
        except (KeyError, TypeError):
            raise TypeError("WidgetWithScript cannot be rendered without an 'id' attribute")

        widget_html = self.render_html(name, value, attrs)
        widget_js = self.render_js_init(id_, name, value)

        out = '{0}<script>{1}</script>'.format(widget_html, widget_js)

        return mark_safe(out)

    def render_html(self, name, value, attrs):
        return super(CustomDateInput, self).render(name, value, attrs)

    def render_js_init(self, id_, name, value):
        return 'initDateChooser({0}, {1});'.format(
            json.dumps(id_),
            json.dumps({'dayOfWeekStart': 1})
            )

class CustomDateTimeInput(widgets.DateTimeInput):
    '''
    Custom widget dat gebruikt wordt voor DateTimeFields.
    Dit widget maakt gebruik van de jquery plugin DateTimePicker
    '''
    def __init__(self, attrs=None, format='%Y-%m-%d %H:%M'):

        super(CustomDateTimeInput, self).__init__(attrs=attrs, format=format)

    def render(self, name, value, attrs=None):

        try:
            id_ = attrs['id']
        except (KeyError, TypeError):
            raise TypeError("WidgetWithScript cannot be rendered without an 'id' attribute")

        widget_html = self.render_html(name, value, attrs)
        widget_js = self.render_js_init(id_, name, value)

        out = '{0}<script>{1}</script>'.format(widget_html, widget_js)

        return mark_safe(out)

    def render_html(self, name, value, attrs):
        return super(CustomDateTimeInput, self).render(name, value, attrs)

    def render_js_init(self, id_, name, value):
        return 'initDateTimeChooser({0}, {1});'.format(
            json.dumps(id_),
            json.dumps({'dayOfWeekStart': 1})
            )

    class Media:

        css = {
            'all': (
                'plugins/datetimepicker/jquery.datetimepicker.min.css',
                )
        }
        js = (
            'plugins/datetimepicker/jquery.datetimepicker.full.min.js',
            'plugins/datetimepicker/custom_script.js'
            )