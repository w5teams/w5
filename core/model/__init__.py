#!/usr/bin/env python
# encoding:utf-8
from core import db


class Users(db.Model):
    __table__ = 'w5_users'
    __timestamps__ = False


class Workflow(db.Model):
    __table__ = 'w5_workflow'
    __timestamps__ = False


class Variablen(db.Model):
    __table__ = 'w5_variablen'
    __timestamps__ = False


class Types(db.Model):
    __table__ = 'w5_type'
    __timestamps__ = False


class Logs(db.Model):
    __table__ = 'w5_logs'
    __timestamps__ = False


class Setting(db.Model):
    __table__ = 'w5_setting'
    __timestamps__ = False


class Report(db.Model):
    __table__ = 'w5_report'
    __timestamps__ = False


class Timer(db.Model):
    __table__ = 'w5_timer'
    __timestamps__ = False


class LoginHistory(db.Model):
    __table__ = 'w5_login_history'
    __timestamps__ = False


class Audit(db.Model):
    __table__ = 'w5_audit'
    __timestamps__ = False


class Nav(db.Model):
    __table__ = 'w5_nav'
    __timestamps__ = False


class Role(db.Model):
    __table__ = 'w5_role'
    __timestamps__ = False


class RoleNav(db.Model):
    __table__ = 'w5_role_nav'
    __timestamps__ = False


class UserRole(db.Model):
    __table__ = 'w5_user_role'
    __timestamps__ = False
