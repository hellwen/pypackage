#! /usr/bin/env python
#coding=utf-8
"""
    account.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, flash, redirect, g\
    , url_for, render_template
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import login_user, logout_user, login_required

from pypackage.extensions import db
from pypackage.models import User, Employee, PrincipalGroup
from pypackage.forms import LoginForm, UserForm, UserEditForm\
    , ChangePasswordForm
from pypackage.base import BaseForm

from flask.ext.weasyprint import HTML, render_pdf, make_flask_url_dispatcher

account = Blueprint("account", __name__, url_prefix="/account")


@account.route("/main/", methods=("GET", "POST"))
@login_required
def main():
    return render_template("account/main.html")


@account.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data,
                                                      form.password.data)

        if user and authenticated and login_user(user,
                remember=form.remember.data):

            return redirect(request.args.get("next") or
                url_for("frontend.index"))
        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)


@account.route("/logout/")
@login_required
def logout():
    logout_user()
    next_url = url_for("account.login")
    return redirect(next_url)


@account.route("/setting/", methods=("GET", "POST"))
@login_required
def setting():
    return render_template("account/setting.html")


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
        form.employee_id.choices = [(g.id, g.emp_name) for g in
            Employee.query.filter_by(active=True).order_by('emp_name')]
        form.principalgroup_id.choices = [(g.id, g.job_name) for g in
            PrincipalGroup.query.filter_by(active=True).order_by('group_name')]
        return form

useradmin = UserAdmin(account, db.session, User, UserForm)


@account.route("/user/list", methods=("GET", "POST"))
@login_required
def user_list():
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
    return useradmin.list_view(column_labels=column_labels)

@account.route('/user/list.pdf')
@login_required
def user_list_pdf():
    html = user_list()
    return render_pdf(HTML(string=html))

@account.route("/user/create/", methods=("GET", "POST"))
@login_required
def user_create():
    return useradmin.create_view()


@account.route("/user/edit/id=<int:id>/", methods=("GET", "POST"))
@login_required
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
@login_required
def user_delete(id):
    return useradmin.delete_view(id)


@account.route("/user/action/", methods=("GET", "POST"))
@login_required
def user_action():
    return useradmin.action_view()


@account.route("/change_password/", methods=("GET", "POST"))
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if g.user.check_password(request.form['password']):
            if request.form['newpassword'] ==\
                request.form['confirm']:
                g.user.password = request.form['newpassword']
                db.session.commit()
                return redirect(url_for('account.setting'))
            else:
                flash(_("New Passwords don't match"), "error")
        else:
            flash(_("Old Password error"), "error")

    return render_template("account/change_password.html", form=form)

