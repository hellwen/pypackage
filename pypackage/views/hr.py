#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.models import Employee, Department, Job, Item
from pypackage.forms import EmployeeForm, DepartmentForm, JobForm

from pypackage.extensions import db
from pypackage.formbase import FormBase


hr = Blueprint('hr', __name__,
    url_prefix="/hr",
    static_folder='static')


@hr.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("hr/main.html")


class JobAdmin(FormBase):
    list_columns = ("job_name", "description")
    fieldsets = [
        (None, {'fields': ('job_name', 'description')}),
    ]
    column_labels = dict(job_name=_("Job"), description=_("Description"))
jobadmin = JobAdmin(hr, db.session, Job, JobForm)


@hr.route("/job/list/", methods=("GET", "POST"))
def job_list():
    return jobadmin.list_view()


@hr.route("/job/view/id=<int:id>", methods=("GET", "POST"))
def job_view(id):
    return jobadmin.show_view(id)


@hr.route("/job/create/", methods=("GET", "POST"))
def job_create():
    return jobadmin.create_view()


@hr.route("/job/edit/id=<int:id>/", methods=("GET", "POST"))
def job_edit(id):
    return jobadmin.edit_view(id)


@hr.route("/job/delete/id=<int:id>/", methods=("GET", "POST"))
def job_delete(id):
    return jobadmin.delete_view(id)


class DeptAdmin(FormBase):
    list_columns = ("dept_name", "description")
    fieldsets = [
        (None, {'fields': ('dept_name', 'description')}),
    ]
    column_labels = dict(dept_name=_("Department"),
        description=_("Description"))
deptadmin = DeptAdmin(hr, db.session, Department, DepartmentForm)


@hr.route("/department/list/", methods=("GET", "POST"))
def department_list():
    return deptadmin.list_view()


@hr.route("/department/id=<int:id>", methods=("GET", "POST"))
def department_view(id):
    return deptadmin.show_view(id)


@hr.route("/department/create/", methods=("GET", "POST"))
def department_create():
    return deptadmin.create_view()


@hr.route("/department/edit/id=<int:id>/", methods=("GET", "POST"))
def department_edit(id):
    return deptadmin.edit_view(id)


@hr.route("/department/delete/id=<int:id>/", methods=("GET", "POST"))
def department_delete(id):
    return deptadmin.delete_view(id)


class EmployeeAdmin(FormBase):
    list_columns = ("emp_code", "emp_name", "gender", "id_card",
        "department", "job")
    column_labels = dict(emp_code=_("Employee Code"),
        emp_name=_("Employee Name"), gender=_("Gender"), id_card=_("ID Card"),
        department=_("Department"), job=_("Job"))
    fieldsets = [
        (None, {'fields': (('emp_code', 'emp_name'),
            ('department_id', 'job_id'), ("remark"))}),
        ("Personal", {'fields': (('gender_id', 'home_addr'),
            ('id_card', 'date_of_birth'))}),
        ("Office", {'fields': (('work_email', 'work_phone'),
            ('work_mobile', 'office_location'))}),
    ]

    def after_create_form(self, form):
        form.department_id.choices = [(g.id, g.dept_name) for g in
            Department.query.filter_by(active=True).
            order_by('dept_name')]
        form.job_id.choices = [(g.id, g.job_name) for g in
            Job.query.filter_by(active=True).
            order_by('job_name')]
        form.gender_id.choices = [(g.item_id, g.item_name) for g in
            Item.query.filter_by(active=True).filter_by(group_id=100).
            order_by('item_order')]

employeeadmin = EmployeeAdmin(hr, db.session, Employee, EmployeeForm)


@hr.route("/employee/list/", methods=("GET", "POST"))
def employee_list():
    return employeeadmin.list_view()


@hr.route("/employee/view/<int:id>/", methods=("GET", "POST"))
def employee_view(id):
    return employeeadmin.show_view(id)


@hr.route("/employee/create/", methods=("GET", "POST"))
def employee_create():
    return employeeadmin.create_view()


@hr.route("/employee/edit/<int:id>/", methods=("GET", "POST"))
def employee_edit(id):
    return employeeadmin.edit_view(id)


@hr.route("/employee/delete/<int:id>/", methods=("GET", "POST"))
def employee_delete(id):
    return employeeadmin.delete_view(id)
