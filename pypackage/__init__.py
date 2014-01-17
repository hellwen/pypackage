#! /usr/bin/env python
#coding=utf-8

from flask import Flask, request, flash, redirect, jsonify, url_for, g,\
    render_template

from flask.ext.babel import Babel, lazy_gettext as _

from pypackage.extensions import db, login_manager, current_user

from pypackage.models import User

from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from pypackage import assets


# init flask assets
assets_env = Environment()


def create_app(object_name=None, env="dev", blueprints=None):

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    configure_extensions(app)
    configure_errorhandlers(app)
    configure_i18n(app)

    configure_blueprints(app)

    return app


def configure_extensions(app):

    db.init_app(app)
    login_manager.setup_app(app)

    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(userid)

    @app.before_request
    def before_request():
        g.user = current_user


def configure_i18n(app):

    babel = Babel(app)

    # @babel.localeselector
    # def get_locale():
    #     # if a user is logged in, use the locale from the user settings
        
    #     # user = getattr(g, 'user', None)
    #     # if user is not None:
    #     #     return user.locale

    #     # otherwise try to guess the language from the user accept
    #     # header the browser transmits.  We support de/fr/en in this
    #     # example.  The best match wins.
    #     accept_languages = app.config.get('ACCEPT_LANGUAGES')
    #     return request.accept_languages.best_match(accept_languages)

    # @babel.timezoneselector
    # def get_timezone():
    #     user = getattr(g, 'user', None)
    #     if user is not None:
    #         return user.timezone


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

    from pypackage.views import frontend, account, hr, base, im, sd, mm

    app.register_blueprint(frontend)
    app.register_blueprint(account)
    app.register_blueprint(base)
    app.register_blueprint(hr)
    app.register_blueprint(im)
    app.register_blueprint(sd)
    app.register_blueprint(mm)


if __name__ == '__main__':
    env = os.environ.get('PRD_ENV', 'dev')
    app = create_app('pypackage.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
