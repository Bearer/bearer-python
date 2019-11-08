import pytest
import requests
import pkg_resources
from unittest.mock import MagicMock

from bearer import Bearer

API_KEY = 'api-key'
BUID = 'buid'

SUCCESS_PAYLOAD = {"data": "It Works!!"}
ERROR_PAYLOAD = {"error": "Oops!"}

URL = 'https://proxy.bearer.sh/{}/'.format(BUID)

CUSTOM_HOST = 'https://example.com'
CUSTOM_URL = '{}/{}/'.format(CUSTOM_HOST, BUID)
ENDPOINT_URL = '{}test?query=param'.format(URL)

HEADERS = {'test': 'header'}
SENT_HEADERS = {
    'Bearer-Proxy-test': 'header',
    'Bearer-Request-Id': 'bearer-request-id'
}
QUERY = {'query': 'param'}
BODY = {'body': 'data'}

VERSION = pkg_resources.require("bearer")[0].version


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
    requests_mock.post(ENDPOINT_URL,
                       headers=SENT_HEADERS,
                       json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.post('/test',
                                headers=HEADERS,
                                query=QUERY,
                                body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD


def test_request_supports_put(requests_mock):
    requests_mock.put(ENDPOINT_URL, headers=SENT_HEADERS, json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.put('/test',
                               headers=HEADERS,
                               query=QUERY,
                               body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD


def test_request_supports_patch(requests_mock):
    requests_mock.patch(ENDPOINT_URL,
                        headers=SENT_HEADERS,
                        json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.patch('/test',
                                 headers=HEADERS,
                                 query=QUERY,
                                 body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD


def test_request_supports_delete(requests_mock):
    requests_mock.delete(ENDPOINT_URL,
                         headers=SENT_HEADERS,
                         json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID)
    response = integration.delete('/test',
                                  headers=HEADERS,
                                  query=QUERY,
                                  body=BODY)

    assert requests_mock.last_request.json() == BODY
    assert response.json() == SUCCESS_PAYLOAD


def test_request_passes_auth_id(requests_mock):
    auth_id = 'test-auth-id'
    expected_headers = {**SENT_HEADERS, 'Bearer-Auth-Id': auth_id}
    requests_mock.post(ENDPOINT_URL,
                       headers=expected_headers,
                       json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID).auth(auth_id)

    response = integration.post('/test',
                                headers=HEADERS,
                                query=QUERY,
                                body=BODY)

    assert response.json() == SUCCESS_PAYLOAD


def test_request_passes_setup_id(requests_mock):
    setup_id = 'test-setup-id'
    expected_headers = {**SENT_HEADERS, 'Bearer-Setup-Id': setup_id}
    requests_mock.post(ENDPOINT_URL,
                       headers=expected_headers,
                       json=SUCCESS_PAYLOAD)

    client = Bearer(API_KEY)
    integration = client.integration(BUID).setup(setup_id)

    response = integration.post('/test',
                                headers=HEADERS,
                                query=QUERY,
                                body=BODY)

    assert response.json() == SUCCESS_PAYLOAD


def test_bearer_with_timeout_parameter_issues_warning():
    with pytest.warns(
            DeprecationWarning,
            match="Please use `http_client_settings`; `timeout` is deprecated"
    ):
        Bearer("api_key", timeout=5)


def test_bearer_with_integration_host_issues_warning():
    with pytest.warns(
            DeprecationWarning,
            match="Please use `host`; `integration_host` is deprecated"):
        Bearer("api_key", integration_host='host')


def test_setting_http_client_settings(mocker):
    request = mocker.patch.object(requests.Session, 'request')
    api = Bearer(API_KEY, http_client_settings={
        "timeout": 11
    }).integration(BUID)
    api.get("/")

    request.assert_called_once_with('GET',
                                    URL,
                                    headers={
                                        'Authorization':
                                        API_KEY,
                                        'User-Agent':
                                        'Bearer-Python ({})'.format(VERSION)
                                    },
                                    json=None,
                                    params=None,
                                    timeout=11)


def test_setting_http_client_settings_in_integration(mocker):
    request = mocker.patch.object(requests.Session, 'request')
    api = Bearer(API_KEY).integration(BUID)
    api.get("/")

    request.assert_called_once_with('GET',
                                    URL,
                                    headers={
                                        'Authorization':
                                        API_KEY,
                                        'User-Agent':
                                        'Bearer-Python ({})'.format(VERSION)
                                    },
                                    json=None,
                                    params=None,
                                    timeout=5)


def test_setting_http_client_settings_in_integration_and_host_in_bearer_class(
        mocker):
    request = mocker.patch.object(requests.Session, 'request')
    github = Bearer(API_KEY, host=CUSTOM_HOST).integration(
        BUID, http_client_settings={"timeout": 11})

    github.get("/")

    request.assert_called_once_with('GET',
                                    CUSTOM_URL,
                                    headers={
                                        'Authorization':
                                        API_KEY,
                                        'User-Agent':
                                        'Bearer-Python ({})'.format(VERSION)
                                    },
                                    json=None,
                                    params=None,
                                    timeout=11)
