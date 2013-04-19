#! /usr/bin/env python
#coding=utf-8
from datetime import datetime

from flask import Blueprint, render_template, g
from flask.ext.babel import gettext as _
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField, DateField

from pypackage.models import InventoryLocation, Item, WarehouseVoucher,\
    WarehouseVoucherProduct, Product, BillRule
from pypackage.forms import InventoryLocationForm, WarehouseVoucherForm,\
    WarehouseVoucherProductForm

from pypackage.extensions import db
from pypackage.base import BaseForm, InlineBaseForm

from pypackage.forms.form import Select2Field

im = Blueprint('im', __name__,
    url_prefix="/im",
    static_folder='static')


@im.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("im/main.html")


class InventoryLocationAdmin(BaseForm):
    list_columns = ("building", "floor", "inventory_type", "location_name")
    column_labels = dict(building=_("Building"),
        floor=_("Floor"),
        inventory_type=_("Inventory Type"),
        location_name=_("Location Name"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("building", "floor"),
            ("inventory_type_id", "location_name"),
            ("remark"))}),
    ]

    def after_create_form(self, form):
        form.inventory_type_id.choices = [(g.item_id, g.item_name) for g in
            Item.query.filter_by(active=True).filter_by(group_id=2).
            order_by('item_order')]
        return form

inventorylocationadmin = InventoryLocationAdmin(im, db.session,
    InventoryLocation, InventoryLocationForm)


@im.route("/inventorylocation/list/", methods=("GET", "POST"))
def inventorylocation_list():
    return inventorylocationadmin.list_view()


@im.route("/inventorylocation/view/<int:id>/", methods=("GET", "POST"))
def inventorylocation_view(id):
    return inventorylocationadmin.show_view(id)


@im.route("/inventorylocation/create/", methods=("GET", "POST"))
def inventorylocation_create():
    return inventorylocationadmin.create_view()


@im.route("/inventorylocation/edit/<int:id>/", methods=("GET", "POST"))
def inventorylocation_edit(id):
    return inventorylocationadmin.edit_view(id)


@im.route("/inventorylocation/delete/<int:id>/", methods=("GET", "POST"))
def inventorylocation_delete(id):
    return inventorylocationadmin.delete_view(id)


class WarehouseVoucherProductAdmin(InlineBaseForm):
    def postprocess_form(self, form):
        form.product_id = Select2Field(_("Product"), default=0,
            choices=[(g.id, g.customer.customer_name + " " + g.product_name) for g in
            Product.query.filter_by(active=True).order_by("customer_id").order_by('product_name')],
            coerce=int, validators=[required()])
        form.inventory_location_id = Select2Field(_("Inventory Location"),
            default=0, choices=[(g.id, g.location_name) for g in
            InventoryLocation.query.filter_by(active=True).
            order_by('location_name')],
            coerce=int, validators=[required()])
        form.quantity = IntegerField(_("Quantity"), validators=[required()])
        return form


class WarehouseVoucherAdmin(BaseForm):
    inline_models = (WarehouseVoucherProductAdmin("products",
        WarehouseVoucherProduct, WarehouseVoucherProductForm),)

    form_create_widget_args = {
        "bill_no": {
            "readonly": "True"
        }
    }

    form_edit_widget_args = {
        "bill_no": {
            "readonly": "True"
        }
    }

    list_columns = ("bill_no", "storage_date", "status", "products")
    column_labels = dict(bill_no=_("Bill No"),
        storage_date=_("Storage Date"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("bill_no", "storage_date"),
            "remark", "products")}),
    ]

    def after_create_form(self, form):
        return form

    def after_create_model(self, model):
        model.bill_no = BillRule().get_new_bill_no("WarehouseVoucher")
        model.opt_datetime = datetime.now()
        model.opt_userid = "demo"
        return model

warehousevoucheradmin = WarehouseVoucherAdmin(im, db.session,
    WarehouseVoucher, WarehouseVoucherForm)


@im.route("/warehousevoucher/list/", methods=("GET", "POST"))
def warehousevoucher_list():
    return warehousevoucheradmin.list_view()


@im.route("/warehousevoucher/view/<int:id>/", methods=("GET", "POST"))
def warehousevoucher_view(id):
    return warehousevoucheradmin.show_view(id)


@im.route("/warehousevoucher/create/", methods=("GET", "POST"))
def warehousevoucher_create():
    return warehousevoucheradmin.create_view()


@im.route("/warehousevoucher/edit/<int:id>/", methods=("GET", "POST"))
def warehousevoucher_edit(id):
    return warehousevoucheradmin.edit_view(id)


@im.route("/warehousevoucher/delete/<int:id>/", methods=("GET", "POST"))
def warehousevoucher_delete(id):
    return warehousevoucheradmin.delete_view(id)
