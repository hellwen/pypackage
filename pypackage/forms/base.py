#! /usr/bin/env python
#coding=utf-8
from wtforms import TextAreaField, HiddenField, TextField
from wtforms.validators import required, optional
from flask.ext.wtf import Form

from flask.ext.babel import lazy_gettext as _


class ItemForm(Form):
    id = HiddenField()
    item_id = TextField(_("Item ID"), validators=[
        required(message=_("You must provide"))])
    item_order = TextField(_("Item Order"), validators=[
        required(message=_("You must provide"))])
    item_name = TextField(_("Item Name"), validators=[
        required(message=_("You must provide"))])


class ItemGroupForm(Form):
    next = HiddenField()

    id = TextField(_("Group ID"), validators=[
        required(message=_("You must provide"))])
    group_name = TextField(_("Group Name"), validators=[
        required(message=_("You must provide"))])
