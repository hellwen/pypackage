#!/usr/bin/env python
#coding=utf-8
from datetime import date

from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField, DateField

from flask.ext.babel import lazy_gettext as _

from .form import Select2Field


class InventoryLocationForm(Form):
    next = HiddenField()

    inventory_type_id = Select2Field(_("Inventory Type"), default=0,
        coerce=int, validators=[required()])
    building = TextField(_("Building#"), validators=[required()])
    floor = IntegerField(_("Floor#"), validators=[required()])
    location_name = TextField(_("Location Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class WarehouseVoucherProductForm(Form):
    id = HiddenField()
    # product_id = Select2Field(_("Product"), default=0,
    #     coerce=int, validators=[required()])
    # inventory_location_id = Select2Field(_("Inventory Location"), default=0,
    #     coerce=int, validators=[required()])
    # quantity = IntegerField(_("Quantity"), validators=[required()])


class WarehouseVoucherForm(Form):
    next = HiddenField()

    bill_no = TextField(_("Bill No"))
    storage_date = DateField(_("Storage Date (eg:2012-01-01)"),
        validators=[required()], default=date.today())
    delivery_person = TextField(_("Delivery Person"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class DeliveryVoucherProductForm(Form):
    id = HiddenField()


class DeliveryVoucherForm(Form):
    next = HiddenField()

    bill_no = TextField(_("Bill No"))
    storage_date = DateField(_("Storage Date (eg:2012-01-01)"),
        validators=[required()], default=date.today())
    consignor = TextField(_("Consignor"), validators=[required()])
    remark = TextAreaField(_("Remark"))
