from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required
from hhservice.web import forms

module = Blueprint('dashboard.stocks.consumptions',
                   __name__,
                   url_prefix='/<stock_id>/consumptions')

app_name = 'stock'


@module.route('')
@login_required
def index(stock_id):
    c = g.get_hhapps_client('stock')
    hhc = g.hhclient
    stock = c.stocks.get(stock_id)
    consumptions = c.consumptions.list(stock)
    for consumption in consumptions:
        consumption.item = c.items.get(consumption.item)
        consumption.consumer = hhc.users.get(consumption.consumer)
    return render_template('/dashboard/stocks/consumptions/index.html',
                           stock=stock,
                           consumptions=consumptions,
                           )
