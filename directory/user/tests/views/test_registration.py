"""
Provide test for implementation of single user registration endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserRegistrationSingle(TestCase):
    """
    Implements test for implementation of single user registration endpoint.
    """

    def test_register_user(self):
        """
        Case: register user with e-mail and password.
        Expect: user with specified e-mail and password is created.
        """
        expected_result = {
            'result': 'User has been created.',
        }
        response = self.client.post('/user/registration/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_register_already_existing_user(self):
        """
        Case: register already existing user with e-mail and password.
        Expect: user with specified e-mail address already exists error message.
        """
        User.objects.create(email='martin.fowler@gmail.com', password='martin.fowler.1337')

        expected_result = {
            'error': 'User with specified e-mail address already exists.',
        }
        response = self.client.post('/user/registration/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
