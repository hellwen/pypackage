#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField, IntegerField

from flask.ext.babel import lazy_gettext as _


class CustomerForm(Form):
    next = HiddenField()

    customer_code = TextField(_("Customer Code"), validators=[required()])
    customer_name = TextField(_("Customer Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))
