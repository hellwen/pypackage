#!/usr/bin/env python
#coding=utf-8

"""
    forms: employee.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from wtforms import TextAreaField, HiddenField, DateField, \
    TextField, ValidationError
from wtforms.validators import required, optional
from flask.ext.wtf import Form

from flask.ext.babel import lazy_gettext as _

from .form import Select2Field


class DepartmentForm(Form):
    next = HiddenField()

    dept_name = TextField(_("Dept Name"), validators=[
        required(message=_("You must provide an department name"))])
    description = TextAreaField(_("Description"))


class JobForm(Form):
    next = HiddenField()

    job_name = TextField(_("Job Name"), validators=[
        required(message=_("You must provide an job name"))])
    description = TextAreaField(_("Description"))


class EmployeeForm(Form):
    next = HiddenField()

    emp_code = TextField(_("Employee Code"), validators=[
        required(message=_("You must provide an employee code"))])
    emp_name = TextField(_("Employee Name"), validators=[
        required(message=_("You must provide an employee name"))])
    work_email = TextField(_("Work Email"))
    work_phone = TextField(_("Work Phone"))
    work_mobile = TextField(_("Work Mobile"))
    office_location = TextField(_("Office Location"))
    department_id = Select2Field(_("Department"), default=0, coerce=int,
        validators=[required(message=_("You must choices a Department"))])
    job_id = Select2Field(_("Job"), default=0, coerce=int,
        validators=[required(message=_("You must choices a Job"))])
    gender_id = Select2Field(_("Gender"), default=0, coerce=int,
        validators=[required(message=_("You must choices a Gender"))])
    id_card = TextField(_("ID Card"))
    home_addr = TextField(_("Home Address"))
    date_of_birth = DateField(_("Date of Birth (eg:2012-01-01)"),
        validators=[optional()])

    remark = TextAreaField(_("Reamrk"))
