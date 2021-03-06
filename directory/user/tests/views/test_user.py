"""
Provide tests for implementation of single user endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from user.models import User


class TestUserSingle(TestCase):
    """
    Implements tests for implementation of single user endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        self.user = User.objects.create_user(
            id=99,
            email='martin.fowler@gmail.com',
            username='martin.fowler',
            password='martin.fowler.1337',
            is_email_confirmed=True,
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'username_or_email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user_token = response.data.get('token')

    def test_get_user_by_username(self):
        """
        Case: get user.
        Expect: user information is returned.
        """
        expected_result = {
            'result': {
                'email': 'martin.fowler@gmail.com',
                'id': 99,
                'is_active': True,
                'is_email_confirmed': True,
                'is_staff': False,
                'is_superuser': False,
                'last_login': None,
                'username': 'martin.fowler',
            },
        }

        response = self.client.get('/users/martin.fowler/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_get_user_by_non_existing_username(self):
        """
        Case: get user by non-existing username.
        Expect: user with specified username does not exist error message.
        """
        expected_result = {
            'error': 'User with specified username does not exist.',
        }

        response = self.client.get('/users/not.martin.fowler/', content_type='application/json')

        assert expected_result == response.json()
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_delete_user_by_username(self):
        """
        Case: delete user.
        Expect: user account is deleted.
        """
        expected_result = {
            'result': 'User has been deleted.',
        }

        response = self.client.delete(
            '/users/martin.fowler/', HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_delete_user_without_deletion_rights(self):
        """
        Case: deleting a user without deletion rights.
        Expect: user has no authority to delete this account by specified username error message.
        """
        expected_result = {
            'error': 'User has no authority to delete this account by specified username.',
        }

        response = self.client.delete(
            '/users/not.martin.fowler/', HTTP_AUTHORIZATION='JWT ' + self.user_token, content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code
