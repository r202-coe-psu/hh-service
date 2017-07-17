
from wtforms import fields
from wtforms import validators

from flask_wtf import FlaskForm

from ..fields import TagListField


class InventoryForm(FlaskForm):
    item = fields.SelectField()
    quantity = fields.IntegerField()
