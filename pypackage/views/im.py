#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.models import Employee, Department, Job, Item
from pypackage.forms import EmployeeForm, DepartmentForm, JobForm

from pypackage.extensions import db
from pypackage.formbase import FormBase


im = Blueprint('im', __name__,
    url_prefix="/im",
    static_folder='static')


@im.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("im/main.html")


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


@im.route("/employee/list/", methods=("GET", "POST"))
def employee_list():
    return employeeadmin.list_view()


@im.route("/employee/view/<int:id>/", methods=("GET", "POST"))
def employee_view(id):
    return employeeadmin.show_view(id)


@im.route("/employee/create/", methods=("GET", "POST"))
def employee_create():
    return employeeadmin.create_view()


@im.route("/employee/edit/<int:id>/", methods=("GET", "POST"))
def employee_edit(id):
    return employeeadmin.edit_view(id)


@im.route("/employee/delete/<int:id>/", methods=("GET", "POST"))
def employee_delete(id):
    return employeeadmin.delete_view(id)
