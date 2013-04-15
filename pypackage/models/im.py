#! /usr/bin/env python
#coding=utf-8
from datetime import datetime

from pypackage.extensions import db

from .base import Item


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), nullable=False, unique=True)
    customer_name = db.Column(db.String(50), nullable=False, unique=True)
    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.customer_name


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), nullable=False, unique=True)
    product_name = db.Column(db.String(50), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    customer = db.relationship(Customer, foreign_keys=customer_id)
    # 类型描述，用于描述该产品的特性，如：外贸、女款等
    type_desc = db.Column(db.String(50))
    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.product_name


class InventoryLocation(db.Model):
    __tablename__ = "inventory_location"

    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.Integer, default=0, nullable=False)
    floor = db.Column(db.Integer, default=0, nullable=False)
    inventory_type_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    inventory_type = db.relationship(Item, foreign_keys=inventory_type_id)
    location_name = db.Column(db.String(50), nullable=False)
    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.location_name


class WarehouseVoucher(db.Model):
    __tablename__ = "warehouse_voucher"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30), nullable=False, unique=True)
    opt_datetime = db.Column(db.Datetime, nullable=False,
        default=datetime.utcnow)
    status = db.Column(db.Integer, default=0, nullable=False)
    remark = db.Column(db.String(300))

    def __repr__(self):
        return self.bill_no


class WarehouseVoucherDtl(db.Model):
    __tablename__ = "warehouse_voucher_dtl"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.Integer, default=0, nullable=False)
    remark = db.Column(db.String(300))

    def __repr__(self):
        return self.bill_no


class DeliveryVoucher(db.Model):
    __tablename__ = "delivery_voucher"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.Integer, default=0, nullable=False)
    remark = db.Column(db.String(300))

    def __repr__(self):
        return self.bill_no
