#! /usr/bin/env python
#coding=utf-8
import sys
from flask import Blueprint, render_template, g
from flask.ext.babel import gettext as _

from pypackage.models import Employee, Department, Job, Item
from pypackage.forms import EmployeeForm, DepartmentForm, JobForm

from pypackage.extensions import db, login_required
from pypackage.base import BaseForm


hr = Blueprint('hr', __name__,
    url_prefix="/hr/job",
    static_folder='static')


class JobAdmin(BaseForm):
    list_columns = ("job_name", "description")
    fieldsets = [
        (None, {'fields': ('job_name', 'description')}),
    ]
    column_labels = dict(job_name=_("Job"), description=_("Description"))
jobadmin = JobAdmin(hr, db.session, Job, JobForm)


@hr.route("/job/list/", methods=("GET", "POST"))
@login_required
def list():
    column_labels = dict(job_name=_("Job"), description=_("Description"))
    return jobadmin.list_view(column_labels=column_labels)


@hr.route("/job/view/id=<int:id>", methods=("GET", "POST"))
@login_required
def view(id):
    return jobadmin.show_view(id)


@hr.route("/job/create/", methods=("GET", "POST"))
@login_required
def create():
    return jobadmin.create_view()


@hr.route("/job/edit/id=<int:id>/", methods=("GET", "POST"))
@login_required
def edit(id):
    return jobadmin.edit_view(id)


@hr.route("/job/delete/id=<int:id>/", methods=("GET", "POST"))
@login_required
def delete(id):
    return jobadmin.delete_view(id)


@hr.route("/job/action/", methods=("GET", "POST"))
@login_required
def action():
    return jobadmin.action_view()

