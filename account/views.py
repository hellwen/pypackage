from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from .models import Account
from .forms import AccountForm

from pypackage.extensions import db
from pypackage.base import FormBase

account = Blueprint('account', __name__, url_prefix="/account")


@account.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("hr/main.html")


class AccountAdmin(FormBase):
    list_columns = ("job_name", "description")
    fieldsets = [
        (None, {'fields': ('job_name', 'description')}),
    ]
    column_labels = dict(job_name=_("Job"), description=_("Description"))
accountadmin = AccountAdmin(account, db.session, Account, AccountForm)


@account.route("/account/", methods=("GET", "POST"))
def job():
    return accountadmin.list_view()


@account.route("/account/view/id=<int:id>", methods=("GET", "POST"))
def job_view(id):
    return accountadmin.show_view(id)


@account.route("/account/create/", methods=("GET", "POST"))
def job_create():
    return accountadmin.create_view()


@account.route("/account/edit/id=<int:id>/", methods=("GET", "POST"))
def job_edit(id):
    return accountadmin.edit_view(id)


@account.route("/account/delete/id=<int:id>/", methods=("GET", "POST"))
def job_delete(id):
    return accountadmin.delete_view(id)

