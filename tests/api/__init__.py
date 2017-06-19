
import unittest
import mongoengine

from hhservice.api import app

class HomeHeroAPITestCase(unittest.TestCase):
    """Parent class of all test cases"""

    def setUp(self):
        self.app = app
        self.app.config['MONGODB_DB'] = 'hhservice_test'
        self.app.testing = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        # Mongoengine keep a global state of the connections that must be
        # reset before each test.
        # Given it doesn't expose any method to get the list of registered
        # connections, we have to do the cleaning by hand...
        mongoengine.connection._connection_settings.clear()
        mongoengine.connection._connections.clear()
        mongoengine.connection._dbs.clear()

    def tearDown(self):
        self.ctx.pop()
        
        if 'mongoengine' in self.app.extensions:
            app.extensions['mongoengine'] = {}
