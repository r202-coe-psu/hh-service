from flask import Blueprint, render_template, g
from hhservice.web import forms

module = Blueprint('dashboard.items.items',
                   __name__,
                   url_prefix='/<stock_id>/items')


@module.route('/add')
def add(item_id):
    c = g.get_hhapps_client('item')
    stock = c.stocks.get(stock_id)
    items = c.stocks.items.list()

    form = forms.stocks.items.ItemForm()

    return render_template('/dashboard/stock/items/add.html',
                           form=form,
                           stock=stock,
                           items=items)
