#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.extensions import db
from pypackage.models import ItemGroup, Item
from pypackage.forms import ItemGroupForm, ItemForm
from pypackage.formbase import FormBase, InlineFormBase


base = Blueprint('base', __name__, url_prefix="/base")


@base.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("base/main.html")


# class ItemInlineAdmin(InlineFormBase):
#     list_columns = ("item_order", "item_name")
#     fieldsets = [
#         (None, {'fields': ('item_order', 'item_name')}),
#     ]
#     column_labels = dict(item_order=_("Order"), item_name=_("Item Name"))


class ItemGroupAdmin(FormBase):
    # inline_models = (ItemInlineAdmin(Item, ItemForm),)

    list_columns = ("group_name", 'items')
    fieldsets = [
        (None, {'fields': ("group_name", 'items')}),
    ]
    column_labels = dict(group_name=_("Group Name"),
        items=_("Items"))

itemgroupadmin = ItemGroupAdmin(base, db.session, ItemGroup, ItemGroupForm)


@base.route("/itemgroup/list/", methods=("GET", "POST"))
def itemgroup_list():
    return itemgroupadmin.list_view()


@base.route("/itemgroup/view/id=<int:id>", methods=("GET", "POST"))
def itemgroup_view(id):
    return itemgroupadmin.show_view(id)


@base.route("/itemgroup/create/", methods=("GET", "POST"))
def itemgroup_create():
    return itemgroupadmin.create_view()


@base.route("/itemgroup/edit/id=<int:id>/", methods=("GET", "POST"))
def itemgroup_edit(id):
    return itemgroupadmin.edit_view(id)


@base.route("/itemgroup/delete/id=<int:id>/", methods=("GET", "POST"))
def itemgroup_delete(id):
    return itemgroupadmin.delete_view(id)
