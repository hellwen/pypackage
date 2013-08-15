#! /usr/bin/env python
#coding=utf-8
from pypackage.extensions import db

from .sd import Customer


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), nullable=False, unique=True)
    product_name = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    customer = db.relationship(Customer, foreign_keys=customer_id)
    specification = db.Column(db.String(50), nullable=True)
    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.product_name
