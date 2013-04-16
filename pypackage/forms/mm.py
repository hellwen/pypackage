#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField

from flask.ext.babel import lazy_gettext as _

from .form import Select2Field


class ProductForm(Form):
    next = HiddenField()

    product_code = TextField(_("Product Code"), validators=[required()])
    product_name = TextField(_("Product Name"), validators=[required()])
    customer_id = Select2Field(_("Customer"), default=0, coerce=int,
        validators=[required()])
    remark = TextAreaField(_("Remark"))
