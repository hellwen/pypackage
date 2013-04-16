#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField, DateField

from flask.ext.babel import lazy_gettext as _

from pypackage.extensions import db
from pypackage.models import WarehouseVoucherProduct
from .fields import InlineModelFormList
from .form import Select2Field


class InventoryLocationForm(Form):
    next = HiddenField()

    building = IntegerField(_("Building#"), validators=[required()])
    floor = IntegerField(_("Floor#"), validators=[required()])
    inventory_type_id = Select2Field(_("Inventory Type"), default=0,
        coerce=int, validators=[required()])
    location_name = TextField(_("Location Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class WarehouseVoucherProductForm(Form):
    next = HiddenField()

    product_id = Select2Field(_("Product"), default=0,
        coerce=int, validators=[required()])
    inventory_location_id = Select2Field(_("Inventory Location"), default=0,
        coerce=int, validators=[required()])
    quantity = IntegerField(_("Quantity"))


class WarehouseVoucherForm(Form):
    next = HiddenField()

    bill_no = TextField(_("Bill No"), validators=[required()])
    storage_date = DateField(_("Storage Date"), validators=[required()])
    products = InlineModelFormList(WarehouseVoucherProductForm,
        db.session, WarehouseVoucherProduct, min_entries=1)
