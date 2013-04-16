#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from pypackage.extensions import db

reload(sys)
sys.setdefaultencoding("utf-8")


class ItemGroup(db.Model):
    __tablename__ = "item_group"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(30), nullable=False)
    items = db.relationship("Item", order_by="Item.id", backref="group",
        cascade="all, delete-orphan")
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.group_name


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column('group_id', db.Integer, db.ForeignKey(ItemGroup.id),
        nullable=False)
    item_id = db.Column('item_id', db.Integer, nullable=False)
    item_order = db.Column('item_order', db.Integer, nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    # def __repr__(self):
    #     return "<%s, %s>" % (str(self.item_id), self.item_name)

    def __repr__(self):
        return self.item_name
