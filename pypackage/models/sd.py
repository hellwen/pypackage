#! /usr/bin/env python
#coding=utf-8
from pypackage.extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), nullable=False, unique=True)
    customer_name = db.Column(db.String(50), nullable=False, unique=True)
    remark = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.customer_name
