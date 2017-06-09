
from .. import app

from . import accounts
app.register_blueprint(accounts.module)
