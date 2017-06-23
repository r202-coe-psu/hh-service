
from flask import g
from flask_login import current_user

from hhclient import Client


def init_request_context(app):
    @app.before_request
    def init_hhclient():
        if g.get('hhclient', None):
            return

        name = None
        password = None
        access_token = None

        user = current_user
        # auth = session.get('auth', None)
        # print(user.data)
        if user.is_authenticated:
            # name = user.name
            # password = auth.get('password', None)
            access_token = user.token.get('access_token', None)

        schemas = app.config.get('HHCLIENT_SCHEMAS', None)
        host = app.config.get('HHCLIENT_HOST')
        port = app.config.get('HHCLIENT_PORT')
        secure = app.config.get('HHCLIENT_SECURE')

        g.hhclient = Client(
                            name=name,
                            password=password,
                            host=host,
                            port=port,
                            secure_connection=secure,
                            access_token=access_token,
                            schemas=schemas)
        if not schemas:
            app.config['HHCLIENT_SCHEMAS'] = g.hhclient.schemas
