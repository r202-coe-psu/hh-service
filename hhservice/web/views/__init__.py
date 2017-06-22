
from . import site
from . import accounts
from . import dashboard


def register_blueprint(app):
    app.register_blueprint(site.module)
    app.register_blueprint(accounts.module)

    dashboard.register_blueprint(app)
