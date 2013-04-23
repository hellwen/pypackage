#! /usr/bin/env python
#coding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user, login_required

__all__ = ['db', 'login_manager', 'current_user', 'login_required']

db = SQLAlchemy()
login_manager = LoginManager()
