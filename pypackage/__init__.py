#! /usr/bin/env python
#coding=utf-8

from flask import Flask, request, flash, redirect, jsonify, url_for, g,\
    render_template

from flask.ext.babel import Babel, gettext as _

from pypackage.extensions import db, login_manager
from pypackage.views import frontend, account, hr, base
from pypackage.models import User


DEFAULT_APP_NAME = 'pypackage'


def create_app(config=None, blueprints=None):

    app = Flask(DEFAULT_APP_NAME)

    if config is not None:
        app.config.from_pyfile(config)

    configure_extensions(app)
    configure_errorhandlers(app)
    configure_i18n(app)

    configure_blueprints(app)

    # configure_modules(app, DEFAULT_MODULES)

    return app


def configure_extensions(app):

    db.init_app(app)
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(userid)


def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return request.accept_languages.best_match(accept_languages)

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone


def configure_errorhandlers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        # if request.is_xhr:
        #     return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)


def configure_blueprints(app):

    app.register_blueprint(frontend)
    app.register_blueprint(account)
    app.register_blueprint(base)
    app.register_blueprint(hr)


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)
