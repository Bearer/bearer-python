import pytest
import requests

from bearer import Bearer, FunctionError

API_KEY = 'api-key'
BUID = 'buid'
FUNCTION_NAME = 'funcName'

SUCCESS_PAYLOAD = {"data": "It Works!!"}
ERROR_PAYLOAD = {"error": "Oops!"}

URL = 'https://int.bearer.sh/api/v4/functions/backend/{}/{}'.format(BUID, FUNCTION_NAME)

CUSTOM_HOST = 'https://example.com'
CUSTOM_URL = '{}/api/v4/functions/backend/{}/{}'.format(CUSTOM_HOST, BUID, FUNCTION_NAME)

def test_invoke_calls_the_function(requests_mock):
    requests_mock.post(URL, json=SUCCESS_PAYLOAD, headers={'Authorization': API_KEY})
    client = Bearer(API_KEY)

    data = client.invoke(BUID, FUNCTION_NAME)

    assert data == SUCCESS_PAYLOAD

def test_invoke_uses_the_integration_host(requests_mock):
    requests_mock.post(CUSTOM_URL, json=SUCCESS_PAYLOAD)
    client = Bearer(API_KEY, integration_host=CUSTOM_HOST)

    data = client.invoke(BUID, FUNCTION_NAME)

    assert data == SUCCESS_PAYLOAD

def test_invoke_raises_on_error_response(requests_mock):
    requests_mock.post(URL, json=ERROR_PAYLOAD)
    client = Bearer(API_KEY)

    with pytest.raises(FunctionError, match='Oops!'):
        client.invoke(BUID, FUNCTION_NAME)
