#!/usr/bin/env python
#coding=utf-8
from wtforms import TextAreaField, HiddenField, TextField              
from wtforms.validators import required, optional
from flask.ext.wtf import Form

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


class CustomerContactForm(Form):
    id = HiddenField()
    name = TextField(_("Name"), validators=[required()])
    title = TextField(_("Title"))
    phone = TextField(_("Phone"))
