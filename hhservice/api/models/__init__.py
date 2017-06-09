
from .users import User

__all__ =[User, ]

import rethinkengine as re

def init_db(**kwargs):
    re.connect(**kwargs)
