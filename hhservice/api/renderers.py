from flask import jsonify
from flask.json import JSONEncoder

import bson
import datetime

def init_json(app):
    app.json_encoder = HHJSONEncoder


class HHJSONEncoder(JSONEncoder):
    def default(self, obj):
        # print('json', obj)
        try:
            if isinstance(obj, bson.ObjectId):
                return str(obj)
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


def render_json(*args, **kwargs):
    """Wrapper around jsonify that sets the Content-Type of the response to
    application/vnd.api+json.
    """
    response = jsonify(*args, **kwargs)
    response.mimetype = 'application/vnd.api+json'
    return response
