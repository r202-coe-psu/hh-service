from . import users
from . import schemas
from . import auth
from . import applications
from . import buildings


def register_blueprint(app):
    app.register_blueprint(auth.module)
    app.register_blueprint(users.module)
    app.register_blueprint(schemas.module)
    app.register_blueprint(buildings.module)
    app.register_blueprint(applications.module)
