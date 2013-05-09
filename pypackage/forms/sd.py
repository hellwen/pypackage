#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form, HiddenField, required,\
    TextAreaField, TextField

from flask.ext.babel import lazy_gettext as _


class CustomerForm(Form):
    next = HiddenField()

    customer_code = TextField(_("Customer Code"), validators=[required()])
    customer_name = TextField(_("Customer Name"), validators=[required()])
    remark = TextAreaField(_("Remark"))


class CustomerShippingForm(Form):
    id = HiddenField()
    name = TextField(_("Name"), validators=[required()])
    address = TextField(_("Address"), validators=[required()])
    remark = TextField(_("Remark"))


class CustomerContactForm(Form):
    id = HiddenField()
    name = TextField(_("Name"), validators=[required()])
    title = TextField(_("Title"), validators=[required()])
    phone = TextField(_("Phone"), validators=[required()])
    mobile = TextField(_("Mobile"), validators=[required()])
    remark = TextField(_("Remark"))
