from datetime import datetime, timezone

from bearer.auth_details import AuthDetails, OAuth1SignatureMethod, TokenType

ACCESS_TOKEN = 'test-access-token'
REFRESH_TOKEN = 'test-refresh-token'
ID_TOKEN = 'test-id-token'
ID_TOKEN_JWT = { 'some': 'id-data' }
RESPONSE_BODY = { 'body': 'data' }
RESPONSE_HEADERS = { 'Content-Type': 'application/json' }
CONSUMER_KEY = 'test-consumer-key'
CONSUMER_SECRET = 'test-secret'
TOKEN_SECRET = 'test-token-secret'
CLIENT_ID = 'test-client-id'
CLIENT_SECRET = 'test-client-secret'

CALLBACK_PARAMS = {
    'oauth_token': 'test-token',
    'oauth_verifier': 'test-verifier'
}

TOKEN_RESPONSE = {
    'body': RESPONSE_BODY,
    'headers': RESPONSE_HEADERS
}

OAUTH1_RAW_DATA = {
    'accessToken': {
        'active': True,
        'value': ACCESS_TOKEN,
        'client_id': CONSUMER_KEY,
        'iat': 1574087265,
        'token_type': 'oauth'
    },
    'callbackParams': CALLBACK_PARAMS,
    'consumerKey': CONSUMER_KEY,
    'consumerSecret': CONSUMER_SECRET,
    'signatureMethod': 'HMAC-SHA1',
    'tokenResponse': TOKEN_RESPONSE,
    'tokenSecret': TOKEN_SECRET
}

OAUTH2_MINIMAL_RAW_DATA = {
    'accessToken': {
        'active': True,
        'value': ACCESS_TOKEN,
        'client_id': CLIENT_ID,
        'iat': 1573661439,
        'token_type': 'bearer'
    },
    'callbackParams': CALLBACK_PARAMS,
    'clientID': CLIENT_ID,
    'clientSecret': CLIENT_SECRET,
    'tokenResponse': TOKEN_RESPONSE
}

OAUTH2_FULL_RAW_DATA = {
    **OAUTH2_MINIMAL_RAW_DATA,
    'accessToken': {
        **OAUTH2_MINIMAL_RAW_DATA['accessToken'],
        'active': False,
        'exp': 1573665039,
        'scope': 'read write'
    },
    'idToken': {
        'active': True,
        'value': ID_TOKEN,
        'client_id': CLIENT_ID,
        'iat': 1573661439,
        'token_type': 'id'
    },
    'idTokenJwt': ID_TOKEN_JWT,
    'refreshToken': {
        'active': True,
        'value': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'iat': 1573661439,
        'scope': 'read write',
        'token_type': 'refresh'
    }
}

def test_oauth1():
    auth_details = AuthDetails(OAUTH1_RAW_DATA)

    assert auth_details.raw_data == OAUTH1_RAW_DATA
    assert auth_details.callback_params == CALLBACK_PARAMS
    assert auth_details.consumer_key == CONSUMER_KEY
    assert auth_details.consumer_secret == CONSUMER_SECRET
    assert auth_details.signature_method == OAuth1SignatureMethod.HMAC_SHA1
    assert auth_details.token_response.body == RESPONSE_BODY
    assert auth_details.token_response.headers == RESPONSE_HEADERS
    assert auth_details.token_secret == TOKEN_SECRET

    access_token = auth_details.access_token

    assert access_token.is_active
    assert access_token.client_id == CONSUMER_KEY
    assert access_token.expires_at is None
    assert access_token.issued_at == datetime(2019, 11, 18, 14, 27, 45, tzinfo=timezone.utc)
    assert access_token.token_type == TokenType.OAUTH1
    assert access_token.value == ACCESS_TOKEN


def test_oauth2_minimal():
    auth_details = AuthDetails(OAUTH2_MINIMAL_RAW_DATA)

    assert auth_details.raw_data == OAUTH2_MINIMAL_RAW_DATA
    assert auth_details.callback_params == CALLBACK_PARAMS
    assert auth_details.client_id == CLIENT_ID
    assert auth_details.client_secret == CLIENT_SECRET
    assert auth_details.id_token is None
    assert auth_details.id_token_jwt is None
    assert auth_details.refresh_token is None
    assert auth_details.token_response.body == RESPONSE_BODY
    assert auth_details.token_response.headers == RESPONSE_HEADERS

    access_token = auth_details.access_token

    assert access_token.is_active
    assert access_token.client_id == CLIENT_ID
    assert access_token.expires_at is None
    assert access_token.issued_at == datetime(2019, 11, 13, 16, 10, 39, tzinfo=timezone.utc)
    assert access_token.scopes == []
    assert access_token.token_type == TokenType.OAUTH2_ACCESS_TOKEN
    assert access_token.value == ACCESS_TOKEN


def test_oauth2_full():
    auth_details = AuthDetails(OAUTH2_FULL_RAW_DATA)

    assert auth_details.raw_data == OAUTH2_FULL_RAW_DATA
    assert auth_details.id_token_jwt == ID_TOKEN_JWT

    access_token = auth_details.access_token

    assert not access_token.is_active
    assert access_token.expires_at == datetime(2019, 11, 13, 17, 10, 39, tzinfo=timezone.utc)
    assert access_token.issued_at == datetime(2019, 11, 13, 16, 10, 39, tzinfo=timezone.utc)
    assert access_token.scopes == ['read', 'write']

    refresh_token = auth_details.refresh_token
    assert refresh_token.client_id == CLIENT_ID
    assert refresh_token.expires_at is None
    assert refresh_token.issued_at == datetime(2019, 11, 13, 16, 10, 39, tzinfo=timezone.utc)
    assert refresh_token.scopes == ['read', 'write']
    assert refresh_token.token_type == TokenType.OAUTH2_REFRESH_TOKEN
    assert refresh_token.value == REFRESH_TOKEN

    id_token = auth_details.id_token
    assert id_token.client_id == CLIENT_ID
    assert id_token.expires_at is None
    assert id_token.issued_at == datetime(2019, 11, 13, 16, 10, 39, tzinfo=timezone.utc)
    assert id_token.scopes is None
    assert id_token.token_type == TokenType.OPENID_CONNECT
    assert id_token.value == ID_TOKEN
