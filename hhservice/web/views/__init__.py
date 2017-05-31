from .. import app

from . import site
from . import accounts

app.register_blueprint(site.module)
app.register_blueprint(accounts.module)
