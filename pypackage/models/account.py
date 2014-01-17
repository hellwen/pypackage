#! /usr/bin/env python
#coding=utf-8

"""
    models: users.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import hashlib

from flask.ext.sqlalchemy import BaseQuery

from pypackage.extensions import db

from .hr import Employee


class PrincipalGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.user_name


class Principal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    principalgroup_id = db.Column(db.Integer, db.ForeignKey(PrincipalGroup.id))
    principalgroup = db.relationship(PrincipalGroup,
        foreign_keys=principalgroup_id,
        backref='principalgroup_id+')
    model_name = db.Column(db.String(50), unique=True)
    add = db.Column(db.Boolean, default=False)
    view = db.Column(db.Boolean, default=False)
    edit = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.model_name


class UserQuery(BaseQuery):
    def authenticate(self, login, password):
        user = self.filter(db.or_(User.username == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    __tablename__ = 'users'

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column("password", db.String(80), nullable=False)
    supperuser = db.Column(db.Boolean, default=False, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(Employee.id))
    employee = db.relationship(Employee,
        foreign_keys=employee_id,
        backref='employee_id+')

    principalgroup_id = db.Column(db.Integer, db.ForeignKey(PrincipalGroup.id))
    principalgroup = db.relationship(PrincipalGroup,
        foreign_keys=principalgroup_id,
        backref='principal_id+')
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __unicode__(self):
        return self.username

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def _get_password(self):
        return self._password
    
    def _set_password(self, password):
        self._password = hashlib.md5(password).hexdigest()
    
    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    @property
    def is_supperuser(self):
        return self.supperuser

    def is_active(self):
        return self.active

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == hashlib.md5(password).hexdigest()
