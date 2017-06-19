import json

from tests.api import HomeHeroAPITestCase

from hhservice import api
from hhservice.api import models


class RegisterTestCase(HomeHeroAPITestCase):
    def setUp(self):
        super().setUp()

        self.app.secret_key = 'hello world'
        api.initial(self.app)

        self.client = self.app.test_client()

        self.register_data = {
            'data': {
                'type': 'users',
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
        user = models.User.objects(
            username=username).first()
        if user:
            user.delete()

        super().tearDown()

    def test_post_register(self):
        response = self.client.post('/users/',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_output = json.loads(response.data)
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'active')

        username = self.register_data['data']['attributes']['username']
        user = models.User.objects(
            username=username).first()

        self.assertIsNotNone(user)
        self.assertTrue(user.verify_password(
            self.register_data['data']['attributes']['password'],
            salt=self.app.secret_key))

    def test_post_duplicate_register(self):
        response = self.client.post('/users/',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')
        response = self.client.post('/users/',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

        json_output = json.loads(response.data)
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'unregister')

    def test_post_email_wrong_should_not_register(self):
        self.register_data['data']['attributes']['email'] = ''
        response = self.client.post('/users/',
                                    data=json.dumps(self.register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

        json_output = json.loads(response.data)
        self.assertEqual(
            json_output['data']['attributes']['status'],
            'unregister')
