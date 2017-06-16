
from .. import app

from . import users
from . import schemas

app.register_blueprint(users.module)
app.register_blueprint(schemas.module)
