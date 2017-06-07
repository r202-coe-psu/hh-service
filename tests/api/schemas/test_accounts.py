import unittest

from hhservice.api.schemas import accounts
import jsonschema

class RegisterSchemaTest(unittest.TestCase):
    def setUp(self):
        self.register_request_dict = dict(
                register=dict(
                    user=dict(
                        username='testuser',
                        password='testpassword',
                        email='test@test.local',
                        first_name='first_name',
                        last_name='last_name'
                        )
                    )
                )

        self.validator = jsonschema.Draft4Validator(accounts.register,
                format_checker=jsonschema.FormatChecker())


    def test_validate_register_schema(self):
        try:
            jsonschema.Draft4Validator.check_schema(accounts.register)
        except Exception as e:
            self.fail(e)
        self.assertTrue(True)
         

    def test_give_valid_case_should_pass(self):
        result = self.validator.is_valid(
                self.register_request_dict['register'])
        
        self.assertTrue(result)


    def test_wrong_email_format_should_not_valid(self):
        self.register_request_dict['register']['user']['email'] = 'test'
        result = self.validator.is_valid(
                self.register_request_dict['register'])

        self.assertFalse(result)


    def test_missing_username_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['register']['user'].pop('username')
        result = self.validator.is_valid(request_dict)
        self.assertFalse(result)

    def test_missing_password_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['register']['user'].pop('password')
        result = self.validator.is_valid(request_dict)
        self.assertFalse(result)


    def test_missing_email_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['register']['user'].pop('email')
        result = self.validator.is_valid(request_dict)
        self.assertFalse(result)


    def test_missing_firstname_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['register']['user'].pop('first_name')
        result = self.validator.is_valid(request_dict)
        self.assertFalse(result)


    def test_missing_lastname_attributes_should_not_valid(self):
        request_dict = self.register_request_dict.copy()
        request_dict['register']['user'].pop('last_name')
        result = self.validator.is_valid(request_dict)
        self.assertFalse(result)



