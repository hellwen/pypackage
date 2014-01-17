#! /usr/bin/env python
#coding=utf-8

import logging

from flask import request, redirect, url_for, render_template, flash
from flask.ext.babel import gettext as _

from pypackage import helpers as h

def expose(url='/', methods=('GET',)):
    """
        Use this decorator to expose views in your view classes.
       
        :param url:                                                                 
            Relative URL for the view
        :param methods:
            Allowed HTTP methods. By default only GET is allowed.
    """
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f
    return wrap


class BaseView(object):

    def __init__(self):
        pass

    def _endpoint(self):
        return self.__class__.__name__

    def _register_urls(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)

            if hasattr(attr, '_urls'):
                for url, methods in attr._urls:
                    self.blueprint.add_url_rule(url,
                            attr_name,
                            attr,
                            methods=methods)


class BaseCRUDView(BaseView):
    
    page_size = 30

    list_template = 'list.html'
    new_template = 'new.html'
    edit_template = 'edit.html'
    show_template = 'show.html'

    def list(self):
        m_data = self.model.query.all()
        m_count = self.model.query.count()

        return self.render('list.html', m_data=m_data, m_count=m_count)

    def new(self):
        return_url = requet.args.get('next',
                url_for('.' + self._endpoint + '_list'))

        m_form = create_form(next=return_url)

        if form.validate_on_submit():
            if create_model(form):
                if '_add_another' in request.form:
                    flash(_('Created successfully.'))
                    return redirect(url_for('.' + self._endpoint + '_create',
                        url=return_url))
                else:
                    return redirect(return_url)

        return self.render('new.html',
                m_form=m_form,
                return_url=return_url)

    def edit(self, id):
        return_url = requet.args.get('next',
                url_for('.' + self._endpoint + '_list'))

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        form = self.edit_form(obj=model)
        if form.validate_on_submit():
            if self.update_model(form, model):
                return redirect(return_url)

        return self.render('edit.html',
                form=form,
                return_url=return_url)

    def show(self, id):
        return_url = requet.args.get('next',
                url_for('.' + self._endpoint + '_list'))

        model = self.get_one(id)

        form = self.edit_form(obj=model)
        return self.render('show.html',
                form=form,
                return_url=return_url)

    def delete(self, id):
        return_url = requet.args.get('next',
                url_for('.' + self._endpoint + '_list'))

        model = self.get_one(id)

        if model:
            self.delete_model(model)

        return redirect(return_url)


