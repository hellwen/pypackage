from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from .models import Account
from .forms import AccountForm

from pypackage.extensions import db
from pypackage.base import FormBase

account = Blueprint('account', __name__,
    url_prefix="/account",
    static_folder='static')


@account.route("/main/", methods=("GET", "POST"))
def main():
    menu = [
        {"": ("Main")},
        {"Account": ("Account", "Other")},
    ]
    return render_template("main.html", menu=menu)


class AccountAdmin(FormBase):
    list_columns = ("user_name", "description")
    fieldsets = [
        (None, {'fields': ('user_name', 'description')}),
    ]
    column_labels = dict(user_name=_("User Name"),
        description=_("Description"))
accountadmin = AccountAdmin(account, db.session, Account, AccountForm)


@account.route("/account_list/", methods=("GET", "POST"))
def account_list():
    return accountadmin.list_view()


@account.route("/account/view/id=<int:id>", methods=("GET", "POST"))
def account_view(id):
    return accountadmin.show_view(id)


@account.route("/account/create/", methods=("GET", "POST"))
def account_create():
    return accountadmin.create_view()


@account.route("/account/edit/id=<int:id>/", methods=("GET", "POST"))
def account_edit(id):
    return accountadmin.edit_view(id)


@account.route("/account/delete/id=<int:id>/", methods=("GET", "POST"))
def account_delete(id):
    return accountadmin.delete_view(id)

