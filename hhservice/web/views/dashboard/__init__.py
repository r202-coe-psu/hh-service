from flask import Blueprint, render_template, g
from flask_login import login_required

from . import applications
from . import buildings
from . import stocks

url_prefix = '/dashboard'
module = Blueprint('dashboard', __name__, url_prefix=url_prefix)


def register_blueprint(app):
    app.register_blueprint(module)

    for view in [applications,
                 buildings]:
        app.register_blueprint(
            view.module,
            url_prefix=url_prefix + view.module.url_prefix)

    for view in [stocks]:
        view.register_blueprint(app, url_prefix)


@module.route('/')
@login_required
def index():
    hhclient = g.hhclient
    hh_stock_client = g.get_hhapps_client('stock')
    buildings = hhclient.buildings.list()
    stocks = hh_stock_client.stocks.list()
    return render_template('dashboard/index.html',
                           buildings=buildings,
                           stocks=stocks)
