
from .users import User
from .buildings import Building
from .applications import Application

__all__ =[User, Application]

from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_db(app):
    db.init_app(app)
