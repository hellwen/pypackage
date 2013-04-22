#! /usr/bin/env python
#coding=utf-8
from datetime import datetime

from flask import Blueprint, render_template, g
from flask.ext.babel import gettext as _
from flask.ext.wtf import required, IntegerField

from pypackage.models import InventoryLocation, Item, Product, BillRule, \
    WarehouseVoucher, WarehouseVoucherProduct, \
    DeliveryVoucher, DeliveryVoucherProduct
from pypackage.forms import InventoryLocationForm,\
    WarehouseVoucherForm, WarehouseVoucherProductForm, \
    DeliveryVoucherForm, DeliveryVoucherProductForm

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


@im.route("/inventorylocation/action/", methods=("GET", "POST"))
def inventorylocation_action():
    return inventorylocationadmin.action_view()


class WarehouseVoucherProductAdmin(InlineBaseForm):
    def postprocess_form(self, form):
        form.product_id = Select2Field(_("Product"), default=0,
            choices=[(g.id, g.customer.customer_name + " " + g.product_name)
            for g in Product.query.filter_by(active=True)
            .order_by("customer_id")
            .order_by('product_name')],
            coerce=int, validators=[required()])
        form.inventory_location_id = Select2Field(_("Inventory Location"),
            default=0, choices=[(g.id, g.location_name) for g in
            InventoryLocation.query.filter_by(active=True).
            order_by('location_name')],
            coerce=int, validators=[required()])
        form.quantity = IntegerField(_("Quantity"), validators=[required()],
            default=1)
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

    list_columns = ("bill_no", "storage_date", "delivery_person", "status",
        "products")
    column_labels = dict(bill_no=_("Bill No"),
        storage_date=_("Storage Date"),
        delivery_person=_("Delivery Person"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("bill_no", "storage_date"),
            ("delivery_person", "remark"),
            "products")}),
    ]
    # actions = [("delete", "Delete"), ("confirm", _("Confirm"))]
    # actions_confirmation = {"delete": _("Confirmation Delete ?"),
    #     "confirm": _("Confirmation Complete ?")}

    def after_create_form(self, form):
        return form

    def after_create_model(self, model):
        model.bill_no = BillRule().get_new_bill_no("WarehouseVoucher")
        model.opt_datetime = datetime.now()
        model.status = "C"
        model.opt_userid = g.user.username
        return model

    # def action_extend(self, action, ids):
    #     if action == "confirm":
    #         for rowid in ids:
    #             model = self.get_one(rowid)
    #             model.status = "C"
    #             self.session.commit()

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


@im.route("/warehousevoucher/action/", methods=("GET", "POST"))
def warehousevoucher_action():
    return warehousevoucheradmin.action_view()


class DeliveryVoucherProductAdmin(InlineBaseForm):
    def postprocess_form(self, form):
        form.product_id = Select2Field(_("Product"), default=0,
            choices=[(g.id, g.customer.customer_name + " " + g.product_name)
            for g in Product.query.filter_by(active=True)
            .order_by("customer_id")
            .order_by('product_name')],
            coerce=int, validators=[required()])
        form.inventory_location_id = Select2Field(_("Inventory Location"),
            default=0, choices=[(g.id, g.location_name) for g in
            InventoryLocation.query.filter_by(active=True).
            order_by('location_name')],
            coerce=int, validators=[required()])
        form.quantity = IntegerField(_("Quantity"), validators=[required()],
            default=1)
        return form


class DeliveryVoucherAdmin(BaseForm):
    inline_models = (DeliveryVoucherProductAdmin("products",
        DeliveryVoucherProduct, DeliveryVoucherProductForm),)

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

    list_columns = ("bill_no", "storage_date", "consignor", "status",
        "products")
    column_labels = dict(bill_no=_("Bill No"),
        storage_date=_("Storage Date"),
        consignor=_("Consignor"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("bill_no", "storage_date"),
            ("consignor", "remark"),
            "products")}),
    ]

    def after_create_form(self, form):
        return form

    def after_create_model(self, model):
        model.bill_no = BillRule().get_new_bill_no("DeliveryVoucher")
        model.opt_datetime = datetime.now()
        model.status = "C"
        model.opt_userid = "demo"
        return model


deliveryvoucheradmin = DeliveryVoucherAdmin(im, db.session,
    DeliveryVoucher, DeliveryVoucherForm)


@im.route("/deliveryvoucher/list/", methods=("GET", "POST"))
def deliveryvoucher_list():
    return deliveryvoucheradmin.list_view()


@im.route("/deliveryvoucher/view/<int:id>/", methods=("GET", "POST"))
def deliveryvoucher_view(id):
    return deliveryvoucheradmin.show_view(id)


@im.route("/deliveryvoucher/create/", methods=("GET", "POST"))
def deliveryvoucher_create():
    return deliveryvoucheradmin.create_view()


@im.route("/deliveryvoucher/edit/<int:id>/", methods=("GET", "POST"))
def deliveryvoucher_edit(id):
    return deliveryvoucheradmin.edit_view(id)


@im.route("/deliveryvoucher/delete/<int:id>/", methods=("GET", "POST"))
def deliveryvoucher_delete(id):
    return deliveryvoucheradmin.delete_view(id)


@im.route("/deliveryvoucher/action/", methods=("GET", "POST"))
def deliveryvoucher_action():
    return deliveryvoucheradmin.action_view()


@im.route("/inventory/list/", methods=("GET", "POST"))
def inventory_list():
    column_labels = dict(product_name=_("Product Name"),
        customer_name=_("Customer Name"),
        quantity=_("Quantity"))

    db.session.query("product_name", "customer_name", "quantity").\
        form_statement(" \
            select p.product_name, c.customer_name, \
                wv.quantity - dv.quantity as quantity  \
            from ( \
                select wvp.product_id, sum(wvp.quantity) as quantity \
                from warehouse_voucher wv \
                inner join warehouse_voucher_product wvp \
                    on wvp.master_id = wv.id \
                where wv.status = 'C' \
                group by wvp.product_id \
                ) wv \
            left join ( \
                select dvp.product_id, sum(dvp.quantity) as quantity \
                from delivery_voucher dv \
                inner join delivery_voucher_product dvp \
                    on dvp.master_id = dv.id \
                where dv.status = 'C' \
                group by dv.product_id \
                ) dv on dv.product_id = wv.product_id \
            inner join products p on p.id = vw.product_id \
            inner join customers c on c.id = p.customer_id \
            ").all()

    return render_template("im/inventory", column_labels)
