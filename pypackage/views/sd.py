#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.models import Customer, CustomerShipping, CustomerContact
from pypackage.forms import CustomerForm, CustomerShippingForm, CustomerContactForm

from pypackage.extensions import db, login_required
from pypackage.base import BaseForm, InlineBaseForm


sd = Blueprint('sd', __name__,
    url_prefix="/sd",
    static_folder='static')


@sd.route("/main/", methods=("GET", "POST"))
@login_required
def main():
    return render_template("sd/main.html")


class CustomerContactInlineAdmin(InlineBaseForm):
    pass


class CustomerShippingInlineAdmin(InlineBaseForm):
    pass


class CustomerAdmin(BaseForm):
    inline_models = (
        CustomerContactInlineAdmin("contacts",
            CustomerContact, CustomerContactForm,
            label=_("Contacts"), min_entries=0),
        CustomerShippingInlineAdmin("shippings",
            CustomerShipping, CustomerShippingForm,
            label=_("Shippings"), min_entries=0),
    )

    list_columns = ("customer_code", "customer_name")
    column_labels = dict(customer_code=_("Customer Code"),
        customer_name=_("Customer Name"),
        remark=_("Remark"),
        active=_("Active"))
    fieldsets = [
        (None, {'fields': (("customer_code", "customer_name"),
            "remark", "contacts", "shippings")}),
    ]

customeradmin = CustomerAdmin(sd, db.session, Customer, CustomerForm)


@sd.route("/customer/list/", methods=("GET", "POST"))
@login_required
def customer_list():
    column_labels = dict(customer_code=_("Customer Code"),
        customer_name=_("Customer Name"),
        remark=_("Remark"),
        active=_("Active"))
    return customeradmin.list_view(column_labels=column_labels)


@sd.route("/customer/view/<int:id>/", methods=("GET", "POST"))
@login_required
def customer_view(id):
    return customeradmin.show_view(id)


@sd.route("/customer/create/", methods=("GET", "POST"))
@login_required
def customer_create():
    return customeradmin.create_view()


@sd.route("/customer/edit/<int:id>/", methods=("GET", "POST"))
@login_required
def customer_edit(id):
    return customeradmin.edit_view(id)


@sd.route("/customer/delete/<int:id>/", methods=("GET", "POST"))
@login_required
def customer_delete(id):
    return customeradmin.delete_view(id)


@sd.route("/customer/action/", methods=("GET", "POST"))
@login_required
def customer_action():
    return customeradmin.action_view()
