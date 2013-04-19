#! /usr/bin/env python
#coding=utf-8

import logging

from flask import request, redirect, url_for, render_template, flash
from flask.ext.babel import gettext as _, ngettext
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField, DateField

from pypackage import helpers as h
from pypackage.forms.fields import InlineModelFormList


class InlineBaseForm(object):
    """
        Settings for inline form administration.

        You can use this class to customize displayed form.
        For example::

            class MyUserInfoForm(InlineFormAdmin):
                form_columns = ('name', 'email')
    """
    _defaults = ['form_columns', 'form_excluded_columns', 'form_args']
    fieldsets = []

    def __init__(self, forward_prop, model, form_class, **kwargs):
        """
            Constructor

            :param model:
                Target model class
            :param kwargs:
                Additional options
        """
        self.forward_prop = forward_prop
        self.model = model
        self.form_class = form_class

        for k in self._defaults:
            if not hasattr(self, k):
                setattr(self, k, None)

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def postprocess_form(self, form_class):
        """
            Post process form. Use this to contribute fields.

            For example::

                class MyInlineForm(InlineFormAdmin):
                    def postprocess_form(self, form):
                        form.value = wtf.TextField('value')
                        return form

                class MyAdmin(ModelView):
                    inline_models = (MyInlineForm(ValueModel),)
        """
        return form_class


class BaseForm(object):
    list_columns = None
    fieldsets = []
    column_labels = dict()
    readonly = False
    set_focus = True
    inline_models = None
    form_create_widget_args = {}
    form_edit_widget_args = {}

    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"

    def __init__(self, blueprint, session, model, form_class):
        self.blueprint = blueprint
        self.session = session
        self.model = model
        self.form_class = form_class
        self.endpoint = model.__name__.lower()

    def get_field_categorys(self):
        return [(tab[0]) for tab in self.fieldsets if tab[0]]

    def is_tuple(self, field):
        return isinstance(field, tuple)

    def render(self, template, **kwargs):
        """
            Render template

            :param template:
                Template path to render
            :param kwargs:
                Template arguments
        """
        # Store self as admin_view
        kwargs['admin_view'] = self
        # kwargs['admin_base_template'] = self.admin.base_template

        # Provide i18n support even if flask-babel is not installed
        # or enabled.
        kwargs['_'] = _
        kwargs['_ngettext'] = ngettext
        kwargs['h'] = h
        kwargs['unicode'] = unicode

        # Contribute extra arguments
        # kwargs.update(self._template_args)

        return render_template(template, **kwargs)

    def get_fields(self, category_name):
        for tab in self.fieldsets:
            if tab[0] == category_name and tab[1]['fields']:
                return tab[1]['fields']

    def get_one(self, id):
        return self.session.query(self.model).get(id)

    def get_form(self):
        pass

    def after_create_form(self, form):
        return form

    def create_form(self, next):
        form = self.get_form()
        if not form:
            if self.inline_models:
                for inline in self.inline_models:
                    child_form = inline.postprocess_form(inline.form_class)
                    setattr(self.form_class, inline.forward_prop,
                            InlineModelFormList(child_form,
                                                self.session,
                                                inline.model,
                                                min_entries=1))

            form = self.form_class(next=next)
        self.after_create_form(form)
        return form

    def edit_form(self, obj):
        form = self.get_form()
        if not form:
            if self.inline_models:
                for inline in self.inline_models:
                    child_form = inline.postprocess_form(inline.form_class)
                    setattr(self.form_class, inline.forward_prop,
                            InlineModelFormList(child_form,
                                                self.session,
                                                inline.model,
                                                min_entries=1))
            form = self.form_class(obj=obj, next=next)
        form = self.after_create_form(form)
        return form

    def after_create_model(self, model):
        return model

    def create_model(self, form):
        try:
            model = self.model()
            form.populate_obj(model)
            model = self.after_create_model(model)
            self.session.add(model)
            self.session.commit()
            return True
        except Exception, ex:
            self.session.rollback()
            flash(_('Failed to create model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to create model')
            return False

    def after_update_model(self, model):
        return model

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            model = self.after_update_model(model)
            self.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to update model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to update model')
            self.session.rollback()
            return False

    def before_delete_model(self, model):
        return True

    def delete_model(self, model):
        try:
            if self.before_delete_model(model):
                self.session.flush()
                self.session.delete(model)
                self.session.commit()
                return True
        except Exception, ex:
            flash(_('Failed to delete model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to delete model')
            self.session.rollback()
            return False

    def list_view(self):
        self.data = self.model.query.all()
        self.count = 0
        return self.render(self.list_template)

    # def show_view(self, id):
    #     self.readonly = True
    #     self.return_url = request.args.get('next',
    #         url_for("." + self.endpoint + "_list"))

    #     obj = self.model.query.get(id)
    #     self.form = self.create_form(obj=obj, next=self.return_url)

    #     return render_template("view.html", formadmin=self,
    #         current_id=id)

    def create_view(self):
        return_url = request.args.get('next',
            url_for("." + self.endpoint + "_list"))

        form = self.create_form(next=return_url)

        # if self.form.validate_on_submit():
        if form.validate_on_submit():
            # if self.create_model(obj):
            if self.create_model(form):
                if '_add_another' in request.form:
                    flash(_('Created successfully.'))
                    return redirect(url_for('.' + self.endpoint + '_create',
                        url=return_url))
                else:
                    return redirect(return_url)

        # return render_template("create.html", formadmin=self)

        return self.render(self.create_template,
                           form=form,
                           form_widget_args=self.form_create_widget_args,
                           return_url=return_url)

    def edit_view(self, id):
        return_url = request.args.get('next',
            url_for("." + self.endpoint + "_list"))

        # if not self.can_edit:
            # return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        form = self.edit_form(obj=model)

        if form.validate_on_submit():
            if self.update_model(form, model):
                return redirect(return_url)

        return self.render(self.edit_template,
                           form=form,
                           form_widget_args=self.form_edit_widget_args,
                           return_url=return_url)

    def delete_view(self, id):
        return_url = request.args.get('next',
            url_for("." + self.endpoint + "_list"))

        model = self.get_one(id)

        if model:
            self.delete_model(model)

        return redirect(return_url)
