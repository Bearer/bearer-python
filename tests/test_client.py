import pytest
import requests

from bearer.Client import Client


def test_client_init():
    client = Client('token')
    assert client.token == 'token'


def test_success_call(requests_mock):
    requests_mock.post(
        'https://int.bearer.sh/api/v3/functions/backend/integrationId/intentTargeted', json={"data": "It Works!!"})
    client = Client('token')
    data = client.call('integrationId', 'intentTargeted')
    assert data == {'data': "It Works!!"}
