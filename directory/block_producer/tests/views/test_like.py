"""
Provide tests for implementation of single block producer like endpoint.
"""
import json
from http import HTTPStatus

from django.test import TestCase

from block_producer.models import (
    BlockProducer,
    BlockProducerLike,
)
from user.models import User


class TestBlockProducerLikeSingle(TestCase):
    """
    Implements tests for implementation of single block producer like endpoint.
    """

    def setUp(self):
        """
        Setup.
        """
        user = User.objects.create_user(email='martin.fowler@gmail.com', password='martin.fowler.1337')
        block_producer = BlockProducer.objects.create(
            user=user,
            name='Block producer Canada',
            website_url='https://bpcanada.com',
            short_description='Founded by a team of serial tech entrepreneurs in Canada.',
        )

        response = self.client.post('/authentication/token/obtaining/', json.dumps({
            'email': 'martin.fowler@gmail.com',
            'password': 'martin.fowler.1337',
        }), content_type='application/json')

        self.user = user
        self.user_token = response.data.get('token')
        self.block_producer = block_producer

    def test_like(self):
        """
        Case: to like block producer.
        Expect: block producer like record is created in database.
        """
        expected_result = {
            'result': 'Block producer liking has been handled.',
        }

        response = self.client.post(
            f'/block-producers/{self.block_producer.id}/like/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert BlockProducerLike.objects.get(user=self.user, block_producer=self.block_producer)
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_unlike(self):
        """
        Case: to nlike block producer.
        Expect: block producer like record is deleted from database.
        """
        BlockProducerLike.objects.create(user=self.user, block_producer=self.block_producer)

        expected_result = {
            'result': 'Block producer liking has been handled.',
        }

        response = self.client.post(
            f'/block-producers/{self.block_producer.id}/like/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert not BlockProducerLike.objects.filter(user=self.user, block_producer=self.block_producer)
        assert expected_result == response.json()
        assert HTTPStatus.OK == response.status_code

    def test_like_non_existing_lock_producer(self):
        """
        Case: to like non-exiting block producer.
        Expect: block producer with specified identifier does not exist error message.
        """
        non_existing_block_producer_id = 100500

        expected_result = {
            'error': 'Block producer with specified identifier does not exist.',
        }

        response = self.client.post(
            f'/block-producers/{non_existing_block_producer_id}/like/',
            HTTP_AUTHORIZATION='JWT ' + self.user_token,
            content_type='application/json',
        )

        assert expected_result == response.json()
        assert HTTPStatus.BAD_REQUEST == response.status_code