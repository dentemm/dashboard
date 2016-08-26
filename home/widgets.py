from __future__ import absolute_import, unicode_literals

import json 

from django.forms import widgets
from django.utils.safestring import mark_safe


class WidgetWithScript(widgets.Widget):
    def render_html(self, name, value, attrs):
        """Render the HTML (non-JS) portion of the field markup"""
        return super(WidgetWithScript, self).render(name, value, attrs)

    def render(self, name, value, attrs=None):
        # no point trying to come up with sensible semantics for when 'id' is missing from attrs,
        # so let's make sure it fails early in the process
        try:
            id_ = attrs['id']
        except (KeyError, TypeError):
            raise TypeError("WidgetWithScript cannot be rendered without an 'id' attribute")

        widget_html = self.render_html(name, value, attrs)

        js = self.render_js_init(id_, name, value)
        out = '{0}<script>{1}</script>'.format(widget_html, js)
    
        return mark_safe(out)

    def render_js_init(self, id_, name, value):
        return ''


class CustomDateTimeInput(widgets.DateTimeInput):
    '''
    Custom widget dat gebruikt wordt voor DateTimeFields.
    Dit widget maakt gebruik van de jquery plugin DateTimePicker
    '''
    def __init__(self, attrs=None, format='%d-%m-%Y %H:%M'):

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