#!/usr/bin/env python
#coding=utf-8

"""
    forms: account.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, HiddenField, TextAreaField, SelectField,\
    TextField, required

from flask.ext.babel import lazy_gettext as _


class AccountForm(Form):
    next = HiddenField()

    user_name = TextField(_("User Name"), validators=[
        required(message=_("You must provide an user name"))])
    accountgroup = SelectField(_("Account Group"))
    description = TextAreaField(_("Description"))
