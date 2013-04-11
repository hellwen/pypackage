#! /usr/bin/env python
#coding=utf-8

from flask.ext.wtf import Form, TextField, HiddenField, required
from flask.ext.babel import gettext as _

from pypackage.extensions import db
from pypackage.models import Item

from .fields import InlineModelFormList


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

    group_name = TextField(_("Group Name"), validators=[
        required(message=_("You must provide"))])
    items = InlineModelFormList(ItemForm, db.session, Item, min_entries=1)

