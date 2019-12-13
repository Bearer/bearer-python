from datetime import datetime, timezone
from enum import Enum

def fromtimestamp_utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)

class OAuth1SignatureMethod(Enum):
    HMAC_SHA1 = 'HMAC-SHA1'
    RSA_SHA1 = 'RSA-SHA1'
    PLAIN_TEXT = 'PLAINTEXT'

class TokenType(Enum):
    OAUTH1 = 'oauth'
    OAUTH2_ACCESS_TOKEN = 'bearer'
    OAUTH2_REFRESH_TOKEN = 'refresh' # Not defined in RFC7662
    OPENID_CONNECT = 'id' # Not defined in RFC7662

class TokenResponse:
  def __init__(self, body: any, headers: dict):
      self.body = body
      self.headers = headers

class TokenData:
    def __init__(self, raw_data: dict):
        token_type = TokenType(raw_data['token_type'])
        expect_scopes = token_type in [
          TokenType.OAUTH2_ACCESS_TOKEN,
          TokenType.OAUTH2_REFRESH_TOKEN
        ]

        self.is_active = raw_data['active']
        self.client_id = raw_data['client_id']
        self.expires_at = fromtimestamp_utc(raw_data['exp']) if 'exp' in raw_data else None
        self.issued_at = fromtimestamp_utc(raw_data['iat'])
        self.scopes = raw_data['scope'].split(' ') if 'scope' in raw_data else ([] if expect_scopes else None)
        self.token_type = token_type
        self.value = raw_data['value']

class AuthDetails:
    def __init__(self, raw_data: dict):
        self.access_token = TokenData(raw_data['accessToken'])
        self.callback_params = raw_data['callbackParams']
        self.client_id = raw_data.get('clientID')
        self.client_secret = raw_data.get('clientSecret')
        self.consumer_key = raw_data.get('consumerKey')
        self.consumer_secret = raw_data.get('consumerSecret')
        self.id_token =  TokenData(raw_data['idToken']) if 'idToken' in raw_data else None
        self.id_token_jwt = raw_data.get('idTokenJwt')
        self.raw_data = raw_data
        self.refresh_token = TokenData(raw_data['refreshToken']) if 'refreshToken' in raw_data else None
        self.token_response = TokenResponse(raw_data['tokenResponse']['body'], raw_data['tokenResponse']['headers'])
        self.token_secret = raw_data.get('tokenSecret')
        self.signature_method = OAuth1SignatureMethod(raw_data['signatureMethod']) if 'signatureMethod' in raw_data else None
