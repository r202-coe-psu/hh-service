
from wtforms import fields
from wtforms import validators

from flask_wtf import FlaskForm

from ..fields import TagListField


class ItemForm(FlaskForm):
    name = fields.TextField('Name', validators=[validators.InputRequired()])
    description = fields.TextField('Description')
    tags = TagListField('Tags')


class ItemUPCForm(FlaskForm):
    upc = fields.TextField('UPC', validators=[validators.InputRequired()])
