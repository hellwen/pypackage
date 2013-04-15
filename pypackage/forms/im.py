#!/usr/bin/env python
#coding=utf-8

"""
    forms: employee.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField


from flask.ext.babel import lazy_gettext as _

from .form import Select2Field


class CustomerForm(Form):
    next = HiddenField()

    customer_code = TextField(_("Customer Code"), validators=[required()])
    customer_code = TextField(_("Customer Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class ProductForm(Form):
    next = HiddenField()

    product_code = TextField(_("Product Code"), validators=[required()])
    product_name = TextField(_("Product Name"), validators=[required()])
    customer_id = Select2Field(_("Customer"), default=0, coerce=int,
        validators=[required()])
    type_desc = TextField(_("Type Desc"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class InventoryLocationForm(Form):
    next = HiddenField()

    building = IntegerField(_("Building#"), validators=[required()])
    floor = IntegerField(_("Floor#"), validators=[required()])
    inventory_type_id = Select2Field(_("Inventory Type"), default=0, coerce=int,
        validators=[required()])
    location_name = TextField(_("Location Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))
