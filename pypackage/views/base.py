#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template
from flask.ext.babel import gettext as _

from pypackage.extensions import db
from pypackage.models import ItemGroup, Item
from pypackage.forms import ItemGroupForm, ItemForm
from pypackage.base import BaseForm
# from pypackage.base import BaseForm, InlineBaseForm


base = Blueprint('base', __name__, url_prefix="/base")


@base.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("base/main.html")


# class ItemInlineAdmin(InlineBaseForm):
#     list_columns = ("item_order", "item_name")
#     fieldsets = [
#         (None, {'fields': ('item_order', 'item_name')}),
#     ]
#     column_labels = dict(item_order=_("Order"), item_name=_("Item Name"))


class ItemGroupAdmin(BaseForm):
    # inline_models = (ItemInlineAdmin(Item, ItemForm),)

    list_columns = ("id", "group_name", 'items')
    fieldsets = [
        (None, {'fields': (("id", "group_name"), "items")}),
    ]
    column_labels = dict(id=_("Group ID"),
        group_name=_("Group Name"),
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


@base.route("/itemgroup/action/", methods=("GET", "POST"))
def itemgroup_action():
    return itemgroupadmin.action_view()


class ItemAdmin(BaseForm):
    # inline_models = (ItemInlineAdmin(Item, ItemForm),)

    list_columns = ("item_id", "item_order", "item_name")
    fieldsets = [
        (None, {'fields': ("item_id", "item_order", "item_name")}),
    ]
    column_labels = dict(item_id=_("Item ID"),
        item_order=_("Item Order"),
        item_name=_("Item Name"))

itemadmin = ItemAdmin(base, db.session, Item, ItemForm)


@base.route("/item/list/", methods=("GET", "POST"))
def item_list():
    return itemadmin.list_view()


@base.route("/item/view/id=<int:id>", methods=("GET", "POST"))
def item_view(id):
    return itemadmin.show_view(id)


@base.route("/item/create/", methods=("GET", "POST"))
def item_create():
    return itemadmin.create_view()


@base.route("/item/edit/id=<int:id>/", methods=("GET", "POST"))
def item_edit(id):
    return itemadmin.edit_view(id)


@base.route("/item/delete/id=<int:id>/", methods=("GET", "POST"))
def item_delete(id):
    return itemadmin.delete_view(id)


@base.route("/item/action/", methods=("GET", "POST"))
def item_action():
    return itemadmin.action_view()

