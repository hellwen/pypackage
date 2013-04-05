from pypackage.extensions import db


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


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    principalgroup_id = db.Column(db.Integer, db.ForeignKey(PrincipalGroup.id))
    principalgroup = db.relationship(PrincipalGroup,
        foreign_keys=principalgroup_id,
        backref='principal_id+')
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.user_name
