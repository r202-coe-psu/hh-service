import unittest
import json

from hhservice.api import app
from hhservice.api import models
import rethinkengine as re


class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        models.init_db(db='hhservice_test')

        self.register_data = {
            'data': {
                'type': 'user',
                'attributes': {
                    'username': 'testuser',
                    'password': 'testpassword',
                    'email': 'test@test.local',
                    'first_name': 'first_name',
                    'last_name': 'last_name'
                }
            }
        }

    def tearDown(self):
        username = self.register_data['data']['attributes']['username']
        user = models.User.objects.filter(
            username=username).first()
        if user:
            user.delete()
        re.disconnect()

    def test_post_register(self):
        response = self.client.post('/register',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_output = json.loads(response.data)[0]
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'active')

    def test_post_duplicate_register(self):
        response = self.client.post('/register',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')
        response = self.client.post('/register',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)

        json_output = json.loads(response.data)[0]
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'unregister')

    def test_post_email_wrong_should_not_register(self):
        self.register_data['data']['attributes']['email'] = ''
        response = self.client.post('/register',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)

        json_output = json.loads(response.data)[0]
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'unregister')
