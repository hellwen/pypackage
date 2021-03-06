#! /usr/bin/env python
#coding=utf-8

from flask.globals import _request_ctx_stack
from flask.ext.babel import lazy_gettext
import helpers as h


class RenderTemplateWidget(object):
    def __init__(self, template):
        self.template = template

    def __call__(self, field, **kwargs):
        ctx = _request_ctx_stack.top
        jinja_env = ctx.app.jinja_env

        kwargs.update({
            'field': field,
            '_': lazy_gettext,
            'h': h,
        })

        template = jinja_env.get_template(self.template)
        return template.render(kwargs)

 
class InlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(InlineFieldListWidget, self).__init__(
            'widgets/inline_field_list.html')


class InlineFormWidget(RenderTemplateWidget):
    def __init__(self):
        super(InlineFormWidget, self).__init__(
            'widgets/inline_form.html')
