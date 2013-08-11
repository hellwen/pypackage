#! /usr/bin/env python
#coding=utf-8
from pypackage.extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), nullable=False, unique=True)
    customer_name = db.Column(db.String(50), nullable=False, unique=True)

    contacts = db.relationship("CustomerContact",
        order_by="CustomerContact.id", backref="customer",
        cascade="all, delete-orphan")
    shippings = db.relationship("CustomerShipping",
        order_by="CustomerShipping.id", backref="customer",
        cascade="all, delete-orphan")

    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.customer_name


class CustomerShipping(db.Model):
    __tablename__ = "customer_shipping"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id),
        nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name


class CustomerContact(db.Model):
    __tablename__ = "customer_contact"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id),
        nullable=False)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __repr__(self):
        return self.name
