#! /usr/bin/env python
#coding=utf-8
from datetime import datetime, date

from pypackage.extensions import db

from .base import Item
from .mm import Product


class InventoryLocation(db.Model):
    __tablename__ = "inventory_location"

    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.Integer, default=0, nullable=False)
    floor = db.Column(db.Integer, default=0, nullable=False)
    inventory_type_id = db.Column(db.Integer, db.ForeignKey(Item.item_id))
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
    storage_date = db.Column(db.Date, nullable=False,
        default=date.today())
    status = db.Column(db.String(1), default="N", nullable=False)
    products = db.relationship("WarehouseVoucherProduct",
        order_by="WarehouseVoucherProduct.id",
        cascade="all, delete-orphan")
    opt_datetime = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    opt_userid = db.Column(db.String(30), nullable=False)
    remark = db.Column(db.String(300))

    def __repr__(self):
        return self.bill_no


class WarehouseVoucherProduct(db.Model):
    __tablename__ = "warehouse_voucher_product"

    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.Integer, db.ForeignKey(WarehouseVoucher.id))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(Product, foreign_keys=product_id)
    inventory_location_id = db.Column(db.Integer,
        db.ForeignKey(InventoryLocation.id))
    inventory_location = db.relationship(InventoryLocation,
        foreign_keys=inventory_location_id)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return u"<%s, %s: %i>" % (self.product.customer.customer_name,
            self.product.product_name, self.quantity)


class DeliveryVoucher(db.Model):
    __tablename__ = "delivery_voucher"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(30), nullable=False, unique=True)
    storage_date = db.Column(db.Date, nullable=False,
        default=date.today())
    status = db.Column(db.String(1), default="N", nullable=False)
    products = db.relationship("DeliveryVoucherProduct",
        order_by="DeliveryVoucherProduct.id",
        cascade="all, delete-orphan")
    opt_datetime = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    opt_userid = db.Column(db.String(30), nullable=False)
    remark = db.Column(db.String(300))

    def __repr__(self):
        return self.bill_no


class DeliveryVoucherProduct(db.Model):
    __tablename__ = "delivery_voucher_product"

    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.Integer, db.ForeignKey(DeliveryVoucher.id))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(Product, foreign_keys=product_id)
    inventory_location_id = db.Column(db.Integer,
        db.ForeignKey(InventoryLocation.id))
    inventory_location = db.relationship(InventoryLocation,
        foreign_keys=inventory_location_id)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return u"<%s, %s: %i>" % (self.product.customer.customer_name,
            self.product.product_name, self.quantity)
