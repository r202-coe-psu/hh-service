import unittest

from hhservice.api.schemas import accounts
import marshmallow as ma


class UserSchemaTest(unittest.TestCase):
    def setUp(self):
        self.register_request_dict = dict(
                data=dict(
                    type='user',
                    attributes=dict(
                        username='testuser',
                        password='testpassword',
                        email='test@test.local',
                        first_name='first_name',
                        last_name='last_name'
                        )
                    )
                )     
        self.schema = accounts.UserSchema()

    def test_give_valid_case_should_pass(self):
        result = self.schema.validate(self.register_request_dict)
        
        self.assertTrue(not result)


    def test_wrong_email_format_should_not_valid(self):
        self.register_request_dict['data']['attributes']['email'] = 'test'
        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)


    def test_missing_username_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['data']['attributes'].pop('username')
        
        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)


    def test_missing_password_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['data']['attributes'].pop('password')

        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)


    def test_missing_email_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['data']['attributes'].pop('email')

        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)


    def test_missing_firstname_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['data']['attributes'].pop('first_name')

        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)



    def test_missing_lastname_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['data']['attributes'].pop('last_name')

        result = None
        with self.assertRaises(ma.exceptions.ValidationError):
            result = self.schema.validate(self.register_request_dict)

        self.assertIsNone(result)



