from pypackage.extensions import db


class Principal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), unique=True)
    add = db.Column(db.Boolean, default=False)
    view = db.Column(db.Boolean, default=False)
    edit = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.user_name


class AccountGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    principal_id = db.Column(db.Integer, db.ForeignKey(Principal.id))
    principal = db.relationship(Principal, foreign_keys=principal_id,
        backref='principal_id+')
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.user_name


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    accountgroup_id = db.Column(db.Integer, db.ForeignKey(AccountGroup.id))
    accountgroup = db.relationship(AccountGroup, foreign_keys=accountgroup_id,
        backref='principal_id+')
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.user_name
