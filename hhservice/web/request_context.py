
import datetime
from dateutil.parser import parse as dateparse

from flask import g, current_app, session
from flask_login import current_user

from hhclient import get_client


def init_request_context(app):
    @app.before_request
    def init_hhclient():
        if g.get('hhclient', None):
            return

        name = None
        password = None
        access_token = None
        expiry_date = None

        user = current_user
        # auth = session.get('auth', None)
        # print(user.data)
        if user.is_authenticated:
            access_token = user.token.get('access-token', None)
            expiry_date = dateparse(user.token.get('expiry-date'))

        schemas = app.config.get('HHCLIENT_SCHEMAS', None)
        host = app.config.get('HHCLIENT_HOST')
        port = app.config.get('HHCLIENT_PORT')
        secure = app.config.get('HHCLIENT_SECURE')

        now = datetime.datetime.utcnow()
        if expiry_date and now > expiry_date:
            refresh_token()
            access_token = session['token']['access-token']

        Client = get_client('hhservice')
        g.hhclient = Client(name=name,
                            password=password,
                            host=host,
                            port=port,
                            secure_connection=secure,
                            access_token=access_token,
                            schemas=schemas)

        if not schemas:
            app.config['HHCLIENT_SCHEMAS'] = g.hhclient.schemas

    @app.before_request
    def init_application_client():

        def get_hhapps_client(name):
            access_token = None
            expiry_date = None

            user = current_user
            if user.is_authenticated:
                access_token = user.token.get('access-token', None)
                expiry_date = dateparse(user.token.get('expiry-date'))
            else:
                return None

            schemas = app.config.get('HHCLIENT_APPS_SCHEMAS', {})
            hhapps = app.config.get('HHCLIENT_APPS_ATTRIBUTES', {})

            now = datetime.datetime.utcnow()
            if expiry_date and now > expiry_date:
                refresh_token()
                access_token = session['token']['access-token']

            if name not in hhapps:
                application = get_application(name)
                hhapps[name] = application.data
                app.config['HHCLIENT_APPS_ATTRIBUTES'] = hhapps
            print('apps', hhapps[name]['publicurl'])

            Client = get_client(name)

            client = Client(api_url=hhapps[name]['publicurl'],
                            access_token=access_token,
                            schemas=schemas.get(name, None))

            if name not in schemas:
                if 'HHCLIENT_APPS_SCHEMAS' not in app.config:
                    app.config['HHCLIENT_APPS_SCHEMAS'] = {}
                app.config['HHCLIENT_APPS_SCHEMAS'][name] = client.schemas

            return client

        g.get_hhapps_client = get_hhapps_client


def get_application(name):
    c = g.hhclient
    application = c.applications.get(name)
    return application


def refresh_token():
    app = current_app
    user = current_user

    schemas = app.config.get('HHCLIENT_SCHEMAS', None)
    host = app.config.get('HHCLIENT_HOST')
    port = app.config.get('HHCLIENT_PORT')
    secure = app.config.get('HHCLIENT_SECURE')
    refresh_token = user.token.get('refresh-token', None)

    if not refresh_token:
        raise Exception()

    Client = get_client('hhservice')
    client = Client(host=host,
                    port=port,
                    secure_connection=secure,
                    access_token=refresh_token,
                    schemas=schemas)

    resource = client.refresh_token()
    user.token.update(resource.data)
    session['token'] = resource.data
