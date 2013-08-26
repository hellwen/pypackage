#! /usr/bin/env python
#coding=utf-8
from datetime import datetime

from flask import Blueprint, render_template, g
from flask.ext.babel import gettext as _

from wtforms import IntegerField
from wtforms.validators import required

from pypackage.models import InventoryLocation, Item, Product, BillRule, \
    WarehouseVoucher, WarehouseVoucherProduct, \
    DeliveryVoucher, DeliveryVoucherProduct
from pypackage.forms import InventoryLocationForm,\
    WarehouseVoucherForm, WarehouseVoucherProductForm, \
    DeliveryVoucherForm, DeliveryVoucherProductForm

from pypackage.extensions import db, login_required
from pypackage.actions import ActionsMixin
from pypackage.base import BaseForm, InlineBaseForm

from pypackage.forms.form import Select2Field

im = Blueprint('im', __name__,
    url_prefix="/im",
    static_folder='static')


@im.route("/main/", methods=("GET", "POST"))
@login_required
def main():
    return render_template("im/main.html")


class InventoryLocationAdmin(BaseForm):
    list_columns = ("inventory_type", "building", "floor", "location_name")
    # column_labels = dict(inventory_type=_("Inventory Type"),
    #     building=_("Building#"),
    #     floor=_("Floor#"),
    #     location_name=_("Location Name"),
    #     remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("building", "floor"),
            ("inventory_type_id", "location_name"),
            ("remark"))}),
    ]

    def after_create_form(self, form):
        form.inventory_type_id.choices = [(g.item_id, g.item_name) for g in
            Item.query.filter_by(active=True).filter_by(group_id=20).
            order_by('item_order')]
        return form

inventorylocationadmin = InventoryLocationAdmin(im, db.session,
    InventoryLocation, InventoryLocationForm)


@im.route("/inventorylocation/list/", methods=("GET", "POST"))
@login_required
def inventorylocation_list():
    column_labels = dict(building=_("Building#"),
        floor=_("Floor#"),
        inventory_type=_("Inventory Type"),
        location_name=_("Location Name"),
        remark=_("Remark"))
    return inventorylocationadmin.list_view(column_labels=column_labels)


@im.route("/inventorylocation/view/<int:id>/", methods=("GET", "POST"))
@login_required
def inventorylocation_view(id):
    return inventorylocationadmin.show_view(id)


@im.route("/inventorylocation/create/", methods=("GET", "POST"))
@login_required
def inventorylocation_create():
    return inventorylocationadmin.create_view()


@im.route("/inventorylocation/edit/<int:id>/", methods=("GET", "POST"))
@login_required
def inventorylocation_edit(id):
    return inventorylocationadmin.edit_view(id)


@im.route("/inventorylocation/delete/<int:id>/", methods=("GET", "POST"))
@login_required
def inventorylocation_delete(id):
    return inventorylocationadmin.delete_view(id)


@im.route("/inventorylocation/action/", methods=("GET", "POST"))
@login_required
def inventorylocation_action():
    return inventorylocationadmin.action_view()


class WarehouseVoucherProductAdmin(InlineBaseForm):
    def postprocess_form(self, form):
        form.product_id = Select2Field(_("Product"), default=0,
            choices=[(g.id, g.customer.customer_name + " "+ g.product_name +
                " " + str(g.specification) + "")
                for g in Product.query.filter_by(active=True)
            .order_by("customer_id")
            .order_by('product_name')],
            coerce=int, validators=[required()])
        form.inventory_location_id = Select2Field(_("Inventory Location"),
            default=0, choices=[(g.id, g.location_full_name) for g in
            InventoryLocation.query.filter_by(active=True).
            order_by('location_name')],
            coerce=int, validators=[required()])
        form.quantity = IntegerField(_("Quantity"), validators=[required()],
            default=1)
        return form


class WarehouseVoucherAdmin(BaseForm):
    inline_models = (WarehouseVoucherProductAdmin("products",
        WarehouseVoucherProduct, WarehouseVoucherProductForm,
        label=_("Products"), min_entries=1),)

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

    list_columns = ("bill_no", "manual_bill_no", "storage_date",
        "delivery_workshop", "store_person", "products")
    column_labels = dict(bill_no=_("Bill No"),
        manual_bill_no=_("Manual Bill No"),
        storage_date=_("Warehouse Voucher Date"),
        delivery_workshop=_("Delivery Workshop"),
        delivery_person=_("Delivery Person"),
        store_person=_("Store Person"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("bill_no", "manual_bill_no"),
            ("storage_date", "delivery_workshop_id"),
            ("store_person", "remark"),
            "products")}),
    ]
    actions = [("delete", _("Delete")), ("confirm", _("Confirm"))]
    actions_confirmation = {"delete": _("Confirmation Delete ?"),
        "confirm": _("Confirmation Complete ?")}

    def after_create_form(self, form):
        form.delivery_workshop_id.choices = \
            [(g.item_id, g.item_name) for g in \
            Item.query.filter_by(active=True).filter_by(group_id=30).
            order_by('item_order')]
        return form

    def after_create_model(self, model):
        model.bill_no = BillRule().get_new_bill_no("WarehouseVoucher")
        model.opt_datetime = datetime.now()
        model.status = "C"
        model.opt_userid = g.user.id
        return model

    def action_extend(self, action, ids):
        if action == "confirm":
            for rowid in ids:
                print rowid
                # model = self.get_one(rowid)
                # model.status = "C"
                # self.session.commit()

warehousevoucheradmin = WarehouseVoucherAdmin(im, db.session,
    WarehouseVoucher, WarehouseVoucherForm)


@im.route("/warehousevoucher/list/", methods=("GET", "POST"))
@login_required
def warehousevoucher_list():
    column_labels = dict(bill_no=_("Bill No"),
        manual_bill_no=_("Manual Bill No"),
        storage_date=_("Warehouse Voucher Date"),
        delivery_workshop=_("Delivery Workshop"),
        store_person=_("Store Person"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    return warehousevoucheradmin.list_view(column_labels=column_labels)


@im.route("/warehousevoucher/view/<int:id>/", methods=("GET", "POST"))
@login_required
def warehousevoucher_view(id):
    return warehousevoucheradmin.show_view(id)


@im.route("/warehousevoucher/create/", methods=("GET", "POST"))
@login_required
def warehousevoucher_create():
    return warehousevoucheradmin.create_view()


@im.route("/warehousevoucher/edit/<int:id>/", methods=("GET", "POST"))
@login_required
def warehousevoucher_edit(id):
    return warehousevoucheradmin.edit_view(id)


@im.route("/warehousevoucher/delete/<int:id>/", methods=("GET", "POST"))
@login_required
def warehousevoucher_delete(id):
    return warehousevoucheradmin.delete_view(id)


@im.route("/warehousevoucher/action/", methods=("GET", "POST"))
@login_required
def warehousevoucher_action():
    return warehousevoucheradmin.action_view()


class DeliveryVoucherProductAdmin(InlineBaseForm):
    def postprocess_form(self, form):
        form.product_id = Select2Field(_("Product"), default=0,
            choices=[(g.id, g.customer.customer_name + " " + g.product_name +
                " " + str(g.specification) + "")
                for g in Product.query.filter_by(active=True)
            .order_by("customer_id")
            .order_by('product_name')],
            coerce=int, validators=[required()])
        form.inventory_location_id = Select2Field(_("Inventory Location"),
            default=0, choices=[(g.id, g.location_full_name) for g in
            InventoryLocation.query.filter_by(active=True).
            order_by('location_name')],
            coerce=int, validators=[required()])
        form.quantity = IntegerField(_("Quantity"), validators=[required()],
            default=1)
        return form


class DeliveryVoucherAdmin(BaseForm):
    inline_models = (DeliveryVoucherProductAdmin("products",
        DeliveryVoucherProduct, DeliveryVoucherProductForm,
        label=_("Products"), min_entries=1),)

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

    list_columns = ("bill_no", "manual_bill_no", "storage_date",
        "picker", "store_person", "products")
    column_labels = dict(bill_no=_("Bill No"),
        manual_bill_no=_("Manual Bill No"),
        storage_date=_("Delivery Voucher Date"),
        picker=_("Picker"),
        store_person=_("Store Person"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    fieldsets = [
        (None, {'fields': (("bill_no", "manual_bill_no"),
            ("storage_date", "picker"),
            ("store_person", "remark"),
            "products")}),
    ]

    def after_create_form(self, form):
        return form

    def after_create_model(self, model):
        model.bill_no = BillRule().get_new_bill_no("DeliveryVoucher")
        model.opt_datetime = datetime.now()
        model.status = "C"
        model.opt_userid = g.user.id
        return model


deliveryvoucheradmin = DeliveryVoucherAdmin(im, db.session,
    DeliveryVoucher, DeliveryVoucherForm)


@im.route("/deliveryvoucher/list/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_list():
    column_labels = dict(bill_no=_("Bill No"),
        manual_bill_no=_("Manual Bill No"),
        storage_date=_("Delivery Voucher Date"),
        picker=_("Picker"),
        store_person=_("Store Person"),
        products=_("Products"),
        status=_("Status"),
        remark=_("Remark"))
    return deliveryvoucheradmin.list_view(column_labels=column_labels)


@im.route("/deliveryvoucher/view/<int:id>/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_view(id):
    return deliveryvoucheradmin.show_view(id)


@im.route("/deliveryvoucher/create/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_create():
    return deliveryvoucheradmin.create_view()


@im.route("/deliveryvoucher/edit/<int:id>/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_edit(id):
    return deliveryvoucheradmin.edit_view(id)


@im.route("/deliveryvoucher/delete/<int:id>/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_delete(id):
    return deliveryvoucheradmin.delete_view(id)


@im.route("/deliveryvoucher/action/", methods=("GET", "POST"))
@login_required
def deliveryvoucher_action():
    return deliveryvoucheradmin.action_view()


@im.route("/inventory/list/", methods=("GET", "POST"))
@login_required
def inventory_list():
    list_columns = ("customer_name", "product_name", "specification",
        "quantity")
    column_labels = dict(product_name=_("Product Name"),
        specification=_("Spec"),
        customer_name=_("Customer Name"),
        quantity=_("Quantity"))

    sql = """
            select p.product_name, p.specification, c.customer_name,
                wv.quantity - coalesce(dv.quantity,0) as quantity
            from (
                select wvp.product_id, sum(wvp.quantity) as quantity
                from warehouse_voucher wv
                inner join warehouse_voucher_product wvp
                    on wvp.master_id = wv.id
                where wv.status = 'C'
                group by wvp.product_id
                ) wv
            left join (
                select dvp.product_id, sum(dvp.quantity) as quantity
                from delivery_voucher dv
                inner join delivery_voucher_product dvp
                    on dvp.master_id = dv.id
                where dv.status = 'C'
                group by dvp.product_id
                ) dv on dv.product_id = wv.product_id
            inner join products p on p.id = wv.product_id
            inner join customers c on c.id = p.customer_id
            where wv.quantity - coalesce(dv.quantity,0) != 0
            """
    data = db.session.execute(sql)
    count = 0

    return render_template("im/inventory.html", endpoint='inventory',
        data=data, count=count,
        list_columns=list_columns, column_labels=column_labels)


@im.route("/inventory_bylocation/list/", methods=("GET", "POST"))
@login_required
def inventory_bylocation_list():
    list_columns = ("product_name", "specification", "customer_name",
        "location_full_name", "quantity")
    column_labels = dict(product_name=_("Product Name"),
        specification=_("Spec"),
        customer_name=_("Customer Name"),
        location_full_name=_("Location Name"),
        quantity=_("Quantity"))

    sql = """
            select p.product_name, p.specification, c.customer_name,
                l.building || l.floor || l.location_name as location_full_name,
                wv.quantity - coalesce(dv.quantity,0) as quantity
            from (
                select wvp.product_id, wvp.inventory_location_id,
                    sum(wvp.quantity) as quantity
                from warehouse_voucher wv
                inner join warehouse_voucher_product wvp
                    on wvp.master_id = wv.id
                where wv.status = 'C'
                group by wvp.product_id, wvp.inventory_location_id
                ) wv
            left join (
                select dvp.product_id, dvp.inventory_location_id,
                    sum(dvp.quantity) as quantity
                from delivery_voucher dv
                inner join delivery_voucher_product dvp
                    on dvp.master_id = dv.id
                where dv.status = 'C'
                group by dvp.product_id, dvp.inventory_location_id
                ) dv on dv.product_id = wv.product_id
                and dv.inventory_location_id = wv.inventory_location_id
            inner join products p on p.id = wv.product_id
            inner join customers c on c.id = p.customer_id
            inner join inventory_location l on l.id = wv.inventory_location_id
            where wv.quantity - coalesce(dv.quantity,0) != 0
            """
    data = db.session.execute(sql)
    count = 0

    return render_template("im/inventory.html",
        endpoint='inventory_bylocation',
        data=data, count=count,
        list_columns=list_columns, column_labels=column_labels)
