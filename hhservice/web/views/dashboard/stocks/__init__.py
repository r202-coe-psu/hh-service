from flask import (Blueprint,
                   render_template,
                   g,
                   redirect,
                   url_for,
                   session,
                   request)
from flask_login import login_required

from hhservice.web import forms

from . import inventories as inventories_view
from . import items as items_view

url_prefix = '/stocks'
module = Blueprint('dashboard.stocks',
                   __name__,
                   url_prefix=url_prefix
                   )

app_name = 'stock'


def register_blueprint(app, parrent_url_prefix):
    prefix = parrent_url_prefix + module.url_prefix
    app.register_blueprint(module, url_prefix=prefix)

    for view in [inventories_view,
                 items_view]:
        app.register_blueprint(
            view.module,
            url_prefix=prefix + view.module.url_prefix)


def get_building(building_id):
    for b in session.get('buildings'):
        if b['id'] == building_id:
            return b


@module.route('')
@login_required
def index():
    c = g.get_hhapps_client(app_name)
    stocks = c.stocks.list()

    return render_template('/dashboard/stocks/index.html',
                           stocks=stocks)


@module.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = forms.stocks.StockForm()
    if not form.validate_on_submit():
        return render_template('dashboard/stocks/create.html',
                               form=form)
    c = g.get_hhapps_client(app_name)
    building = get_building(request.args.get('building_id'))

    stock = c.stocks.create(building=building,
                            **form.data)

    if stock.is_error:
        return render_template('dashboard/stocks/create.html',
                               form=form,
                               errors=stock.errors)

    return redirect(url_for('dashboard.stocks.view',
                            stock_id=stock.id))


@module.route('/<stock_id>')
@login_required
def view(stock_id):

    c = g.get_hhapps_client(app_name)
    stock = c.stocks.get(stock_id)
    inventories = c.inventories.list(stock)
    available_items = inventories_view.get_available_items(inventories)

    return render_template('/dashboard/stocks/view.html',
                           stock=stock,
                           available_items=available_items,
                           inventories=inventories)


@module.route('/<stock_id>')
@login_required
def delete(stock_id):
    return redirect()
