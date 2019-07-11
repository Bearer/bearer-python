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


PROXY_URL = 'https://int.bearer.sh/api/v4/functions/backend/{}/bearer-proxy'.format(BUID)
ENDPOINT_URL = '{}/test?query=param'.format(PROXY_URL)

HEADERS = { 'test': 'header' }
SENT_HEADERS = { 'Bearer-Proxy-test': 'header' }
QUERY = { 'query': 'param' }
BODY = { 'body': 'data' }

def test_request_supports_get(requests_mock):
    requests_mock.get(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.get('/test', headers=HEADERS, query=QUERY)

    assert response.json() == SUCCESS_PAYLOAD

def test_request_supports_head(requests_mock):
    requests_mock.head(ENDPOINT_URL, headers=SENT_HEADERS)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.head('/test', headers=HEADERS, query=QUERY)

    assert response.status_code == 200

def test_request_supports_post(requests_mock):
    requests_mock.post(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.post('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD

def test_request_supports_put(requests_mock):
    requests_mock.put(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.put('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD

def test_request_supports_patch(requests_mock):
    requests_mock.patch(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.patch('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD

def test_request_supports_delete(requests_mock):
    requests_mock.delete(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.delete('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD

def test_request_passes_auth_id(requests_mock):
    auth_id = 'test-auth-id'
    expected_headers = { **SENT_HEADERS, 'Bearer-Auth-Id': auth_id }
    requests_mock.post(ENDPOINT_URL, headers=expected_headers, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID).auth(auth_id)

    response = integration.post('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert response.json() == SUCCESS_PAYLOAD

def test_request_passes_setup_id(requests_mock):
    setup_id = 'test-setup-id'
    expected_headers = { **SENT_HEADERS, 'Bearer-Setup-Id': setup_id }
    requests_mock.post(ENDPOINT_URL, headers=expected_headers, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID).setup(setup_id)

    response = integration.post('/test', headers=HEADERS, query=QUERY, body=BODY)

    assert response.json() == SUCCESS_PAYLOAD
