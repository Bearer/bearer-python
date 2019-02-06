import os
import time
import pytest

from bearer.Client import Client


def test_client_init():
    client = Client('token')
    assert client.token == 'token'
