#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.models import Product, Customer
from pypackage.forms import ProductForm

from pypackage.extensions import db, login_required
from pypackage.base import BaseForm


mm = Blueprint('mm', __name__,
    url_prefix="/mm",
    static_folder='static')


@mm.route("/main/", methods=("GET", "POST"))
@login_required
def main():
    return render_template("mm/main.html")


class ProductAdmin(BaseForm):
    list_columns = ("product_code", "product_name", "customer")
    column_labels = dict(product_code=_("Product Code"),
        product_name=_("Product Name"),
        customer=_("Customer"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (('product_code', 'product_name'),
            'customer_id', "remark")}),
    ]

    def after_create_form(self, form):
        form.customer_id.choices = [(g.id, g.customer_code + " - " + g.customer_name) for g in
            Customer.query.filter_by(active=True).
            order_by('customer_name')]
        return form

productadmin = ProductAdmin(mm, db.session, Product, ProductForm)


@mm.route("/product/list/", methods=("GET", "POST"))
@login_required
def product_list():
    return productadmin.list_view()


@mm.route("/product/view/<int:id>/", methods=("GET", "POST"))
@login_required
def product_view(id):
    return productadmin.show_view(id)


@mm.route("/product/create/", methods=("GET", "POST"))
@login_required
def product_create():
    return productadmin.create_view()


@mm.route("/product/edit/<int:id>/", methods=("GET", "POST"))
@login_required
def product_edit(id):
    return productadmin.edit_view(id)


@mm.route("/product/delete/<int:id>/", methods=("GET", "POST"))
@login_required
def product_delete(id):
    return productadmin.delete_view(id)


@mm.route("/product/action/", methods=("GET", "POST"))
@login_required
def product_action():
    return productadmin.action_view()

