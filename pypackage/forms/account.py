#!/usr/bin/env python
#coding=utf-8

"""
    forms: account.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextAreaField, HiddenField, BooleanField, \
        PasswordField, SubmitField, TextField, ValidationError, SelectField, \
        required, optional, equal_to, regexp

from flask.ext.babel import gettext, lazy_gettext as _

from pypackage.models import User

from .validators import is_username


class LoginForm(Form):
    next = HiddenField()
    
    login = TextField(_("User"), validators=[
        required(message=_("You must provide an email or username"))])
    password = PasswordField(_("Password"), validators=[
        required(message=_("You must provide an password"))])
    remember = BooleanField(_("Remember me"))

    submit = SubmitField(_("Login"))


class UserForm(Form):
    next = HiddenField()

    username = TextField(_("User name"), validators=[
                         required(message=_("User name required")),
                         is_username])
    password = PasswordField(_("Password"), validators=[
        required(message=_("Password required"))])
    password_again = PasswordField(_("Password again"), validators=[
        equal_to("password", message=_("Passwords don't match"))])

    supperuser = BooleanField("Supper User")

    employee_id = SelectField(_("Employee"), default=0, coerce=int,
        validators=[optional()])
    principalgroup_id = SelectField(_("Principal Group"), default=0,
        coerce=int, validators=[optional()])

    description = TextField(_("Description"))

    active = BooleanField("Active")

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError, gettext("This username is taken")


class UserEditForm(Form):
    next = HiddenField()

    username = TextField(_("User name"), validators=[
                         required(message=_("User name required")),
                         is_username])

    supperuser = BooleanField("Supper User")

    employee_id = SelectField(_("Employee"), default=0, coerce=int,
        validators=[optional()])
    principalgroup_id = SelectField(_("Principal Group"), default=0,
        coerce=int, validators=[optional()])

    description = TextField(_("Description"))

    active = BooleanField("Active")
