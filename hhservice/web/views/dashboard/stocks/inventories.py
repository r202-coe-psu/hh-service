from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required
from hhservice.web import forms

module = Blueprint('dashboard.stocks.inventories',
                   __name__,
                   url_prefix='/<stock_id>/inventories')

app_name = 'stock'


def get_available_items(inventories):
    c = g.get_hhapps_client(app_name)
    available_items = {}
    for inventory in inventories:
        available_item = available_items.get(inventory.item, None)
        if available_item:
            available_items[inventory.item]['available_serving_size'] += \
                    inventory.available_serving_size
        else:
            item = c.items.get(inventory.item)
            available_items[item.id] = dict(
                    item=item,
                    available_serving_size=inventory.available_serving_size)

    return available_items


@module.route('')
@login_required
def index(stock_id):
    c = g.get_hhapps_client('stock')
    stock = c.stocks.get(stock_id)
    inventories = c.inventories.list(stock)
    for inventory in inventories:
        inventory.item = c.items.get(inventory.item)
    return render_template('/dashboard/stocks/inventories/index.html',
                           stock=stock,
                           inventories=inventories,
                           )


@module.route('/add', methods=['GET', 'POST'])
@login_required
def add(stock_id):
    c = g.get_hhapps_client('stock')
    stock = c.stocks.get(stock_id)
    items = c.items.list()

    item_choices = [(item.id, '{} ({})'.format(item.name, item.upc)) for item
                    in items]
    item_choices.insert(0, ('', 'Select item or enter UPC'))
    form = forms.stocks.inventories.InventoryForm()
    form.item.choices = item_choices
    form.expired_date.label.text = '{}: default date is {}'.format(
            form.expired_date.label.text,
            form.expired_date.default.ctime())
    # if not form.expired_date.data:
    #     form.expired_date.data = form.expired_date.default.strftime(
    #             form.expired_date.format)

    is_item = True if form.item.data else False or len(form.item_upc.data) > 0
    if not form.validate_on_submit():
        errors = [{'detail': '{}: {}'.format(k, v)} for k, v
                  in form.errors.items()]
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               stock=stock,
                               items=items)
    if not is_item:
        errors = [{'detail': 'Select item or enter upc'}]
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               errors=errors,
                               stock=stock,
                               items=items)
    data = form.data
    if len(data['item']) > 0:
        data['item'] = {'id': data['item']}

    inventory = c.inventories.create(stock=stock, **data)
    if inventory.is_error:
        # import pprint
        # pprint.pprint(inventory.data)
        return render_template('/dashboard/stocks/inventories/add.html',
                               form=form,
                               stock=stock,
                               items=items)

    return redirect(url_for('dashboard.stocks.inventories.index',
                            stock_id=stock.id))


@module.route('/consume', methods=['GET', 'POST'])
@login_required
def consume(stock_id):
    c = g.get_hhapps_client('stock')
    stock = c.stocks.get(stock_id)
    # items = c.inventories.list_items(stock)
    inventories = c.inventories.list(stock)
    available_items = get_available_items(inventories)
    print('available_items:', available_items)
    form = forms.stocks.inventories.InventoryConsumingForm()
    item_choices = [
            (aitem['item'].id,
             '{} ({}) available serving size: {}'.format(
                    aitem['item'].name,
                    aitem['item'].upc,
                    aitem['available_serving_size']))
            for k, aitem in available_items.items()]

    item_choices.insert(0, ('', 'Select item'))
    form.item.choices = item_choices
    print(form.item.data, type(form.item.data))

    if (not form.validate_on_submit()) or (len(form.item.data) == 0):
        errors = [{'detail': '{}: {}'.format(k, v)} for k, v
                  in form.errors.items()]
        return render_template('/dashboard/stocks/inventories/consume.html',
                               form=form,
                               errors=errors,
                               stock=stock)
    print(form.data)
    c.inventories.consume(stock=stock,
                          item=form.item.data,
                          consuming_size=form.consuming_size.data)
    return redirect(url_for('dashboard.stocks.inventory.index',
                            stock_id=stock.id))
