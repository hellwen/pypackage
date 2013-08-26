#!/usr/bin/env python
#coding=utf-8

"""
    forms: account.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from wtforms import TextAreaField, HiddenField, BooleanField, \
    PasswordField, SubmitField, TextField, ValidationError
from wtforms.validators import required, optional, equal_to
from flask.ext.wtf import Form

from flask.ext.babel import lazy_gettext as _

from pypackage.models import User

from .validators import is_username
from .form import Select2Field


class LoginForm(Form):
    next = HiddenField()
    
    login = TextField(_("User"), validators=[
        required(message=_("You must provide an username"))])
    password = PasswordField(_("Password"), validators=[
        required(message=_("You must provide an password"))])
    remember = BooleanField(_("Remember me"))

    submit = SubmitField(_("Login"))

class ChangePasswordForm(Form):
    next = HiddenField()

    password = PasswordField(_('Old Password'), validators=[
        required(message=_("Password required"))])
    newpassword = PasswordField(_('New Password'), validators=[
        required(message=_("Password required"))])
    confirm  = PasswordField(_('Repeat Password'), validators=[
        required(message=_("Password required"))])

class UserForm(Form):
    next = HiddenField()

    username = TextField(_("User name"), validators=[
                         required(message=_("User name required")),
                         is_username])
    password = PasswordField(_("Password"), validators=[
        required(message=_("Password required"))])
    password_again = PasswordField(_("Password again"), validators=[
        equal_to("password", message=_("Passwords don't match"))])

    supperuser = BooleanField(_("Supper User"), default=False)

    employee_id = Select2Field(_("Employee"), default=0, coerce=int,
        validators=[optional()])
    principalgroup_id = Select2Field(_("Principal Group"), default=0,
        coerce=int, validators=[optional()])

    description = TextAreaField(_("Description"))

    active = BooleanField(_("Active"), default=True,
         validators=[required()])

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError, _("This username is taken")


class UserEditForm(Form):
    next = HiddenField()

    username = TextField(_("User name"), validators=[
                         required(message=_("User name required")),
                         is_username])

    supperuser = BooleanField(_("Supper User"), default=False)

    employee_id = Select2Field(_("Employee"), default=0, coerce=int,
        validators=[optional()])
    principalgroup_id = Select2Field(_("Principal Group"), default=0,
        coerce=int, validators=[optional()])

    description = TextAreaField(_("Description"))

    active = BooleanField(_("Active"), default=True,
         validators=[required()])
