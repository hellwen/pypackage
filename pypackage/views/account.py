#! /usr/bin/env python
#coding=utf-8
"""
    account.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask.ext.babel import gettext as _
from flask.ext.login import login_user, logout_user, login_required

from pypackage.extensions import db
from pypackage.models import User, Employee, PrincipalGroup
from pypackage.forms import LoginForm, UserForm, UserEditForm
from pypackage.base import BaseForm


account = Blueprint("account", __name__, url_prefix="/account")


@account.route("/main/", methods=("GET", "POST"))
@login_required
def main():
    return render_template("account/main.html")


@account.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data,
                                                      form.password.data)

        if user and authenticated and login_user(user,
                remember=form.remember.data):

            flash(_("Welcome back, %(name)s", name=user.username), "success")

            return redirect(request.args.get("next") or
                url_for("frontend.index"))
        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)


@account.route("/logout/")
@login_required
def logout():
    logout_user()
    flash(_("You are now logged out"), "success")
    next_url = url_for("frontend.index")
    return redirect(next_url)


class UserAdmin(BaseForm):
    list_columns = ("username", "supperuser", "employee",
        "principalgroup", "description")
    fieldsets = [
        (None, {'fields': (('username', "password", "password_again"),)}),
        (_("Auth"), {'fields': (
            ("employee_id", "supperuser", "principalgroup_id"),
            ("description", "active"),)}),
    ]
    column_labels = dict(username=_("User Name"),
        password=_("Password"),
        password_again=_("Password Again"),
        employee=_("Employee"),
        employee_id=_("Employee"),
        supperuser=_("Supper User"),
        principalgroup=_("Principal Group"),
        principalgroup_id=_("Principal Group"),
        description=_("Description"),
        active=_("Active"))

    def after_create_form(self, form):
        form.employee_id.choices = [(g.id, g.dept_name) for g in
            Employee.query.filter_by(active=True).order_by('emp_name')]
        form.principalgroup_id.choices = [(g.id, g.job_name) for g in
            PrincipalGroup.query.filter_by(active=True).order_by('group_name')]

useradmin = UserAdmin(account, db.session, User, UserForm)


@account.route("/user/list", methods=("GET", "POST"))
def user_list():
    return useradmin.list_view()


@account.route("/user/create/", methods=("GET", "POST"))
def user_create():
    return useradmin.create_view()


@account.route("/user/edit/id=<int:id>/", methods=("GET", "POST"))
def user_edit(id):
    class UserEditAdmin(UserAdmin):
        fieldsets = [
            (None, {'fields': (("username"),)}),
            (_("Auth"), {'fields': (
                ("employee_id", "supperuser", "principalgroup_id"),
                ("description", "active"),)}),
        ]

    usereditadmin = UserEditAdmin(account, db.session, User, UserEditForm)

    return usereditadmin.edit_view(id)


@account.route("/user/delete/id=<int:id>/", methods=("GET", "POST"))
def user_delete(id):
    return useradmin.delete_view(id)


# @account.route("/user/create/", methods=("GET", "POST"))
# def user_create():
#     form = UserForm(next=request.args.get('next', None))

#     # form.employee.choices = [(1, "1"),]
#     # form.employee.choices.extend([(g.id, g.dept_name) for g in
#         # Employee.query.filter_by(active=True).order_by('emp_name')])

#     if form.validate_on_submit():
#         user = User()
#         form.populate_obj(user)

#         db.session.add(user)
#         db.session.commit()

#         flash(_("Welcome, %(name)s", name=user.username), "success")

#         next_url = form.next.data

#         if not next_url or next_url == request.path:
#             next_url = url_for('account.main', username=user.username)

#         return redirect(next_url)

#     return render_template("account/user.html", form=form)


# @account.route("/user/edit=<int:id>/", methods=("GET", "POST"))
# def user_edit(id):
#     user = User.query.get(id)
#     form = UserForm(next=request.args.get('next', None), obj=user)

#     form.employee_id.choices = [(0, "")]
#     form.employee_id.choices.extend([(g.id, g.dept_name) for g in
#         Employee.query.filter_by(active=True).order_by('emp_name')])

#     if form.validate_on_submit():
#         form.populate_obj(user)
#         db.session.add(user)
#         db.session.commit()

#         next_url = form.next.data
#         if not next_url or next_url == request.path:
#             next_url = url_for('account.main')

#         return redirect(url_for('account.user'))

#     return render_template("account/user.html", form=form)


# @account.route("/user/delete=<int:id>/", methods=("GET", "POST"))
# def user_delete(id):
#     user = User.query.get(id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#     return redirect(url_for("account.user"))
