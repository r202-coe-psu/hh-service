
from . import users
from . import schemas
from . import auth


def register_blueprint(app):
    app.register_blueprint(users.module)
    app.register_blueprint(schemas.module)
    app.register_blueprint(auth.module)
