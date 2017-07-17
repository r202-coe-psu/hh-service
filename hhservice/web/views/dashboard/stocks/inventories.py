from flask import Blueprint, render_template, g
from hhservice.web import forms

module = Blueprint('dashboard.stocks.inventories',
                   __name__,
                   url_prefix='/<stock_id>/inventories')


@module.route('/add')
def add(stock_id):
    c = g.get_hhapps_client('stock')
    stock = c.stocks.get(stock_id)
    items = c.items.list()

    form = forms.stocks.inventories.InventoryForm()

    return render_template('/dashboard/stocks/inventories/add.html',
                           form=form,
                           stock=stock,
                           items=items)
