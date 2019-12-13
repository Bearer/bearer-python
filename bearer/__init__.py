"""
Bearer Python bindings
"""

from typing import Optional, Union, Dict
from logging import DEBUG, INFO
from textwrap import dedent

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import warnings
import requests
import pkg_resources
import logging

from .auth_details import AuthDetails
from .errors import MissingAuthId

# Bearer Python bindings
# API docs at https://docs.bearer.sh/integration-clients/python
# Authors:
# Bearer Team <dev@bearer.sh>

BEARER_AUTH_HOST = 'https://auth.bearer.sh'
BEARER_PROXY_HOST = 'https://proxy.bearer.sh'
TIMEOUT = 5
DEFAULT_RETRY = 1

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)


class Bearer():
    """Bearer client

    Example:
      >>> from bearer import Bearer
      >>>
      >>> bearer = Bearer('<api-key>')
      >>> bearer.integration('<integration_id>')
    """
    def __init__(self,
                 secret_key: str,
                 integration_host: str = None,
                 timeout: int = None,
                 auth_host: str = BEARER_AUTH_HOST,
                 host: str = BEARER_PROXY_HOST,
                 http_client_settings: Dict[str, str] = {"timeout": TIMEOUT}):
        """
        Args:
          secret_key: developer API Key from https://app.bearer.sh/settings
          auth_host: used internally
          host: used internally
          http_client_settings: Dictionary passed as kwargs to requests.request method
          timeout: DEPRECATED please use http_client_settings instead
          integration_host: DEPRECATED please use host instead
        """
        self.secret_key = secret_key
        self.auth_host = auth_host
        self.host = host
        self.http_client_settings = http_client_settings
        if integration_host is not None:
            warnings.warn(
                "Please use `host`; `integration_host` is deprecated",
                DeprecationWarning)
            self.host = integration_host
        if timeout is not None:
            warnings.warn(
                "Please use `http_client_settings`; `timeout` is deprecated",
                DeprecationWarning)
            self.timeout = self.http_client_settings["timeout"] = timeout

    def integration(self,
                    integration_id: str,
                    http_client_settings: Dict[str, str] = {}):
        client_settings = {**self.http_client_settings, **http_client_settings}
        return Integration(integration_id, self.auth_host, self.host,
                           self.secret_key, client_settings)


BodyData = Union[dict, list]


class Integration():
    def __init__(
            self,
            integration_id: str,
            auth_host: str,
            host: str,
            secret_key: str,
            http_client_settings: Dict[str, str] = {},
            auth_id: str = None,
            setup_id: str = None,
    ):
        """
        Args:
          integration_id: id of an integration, see https://app.bearer.sh/apis
          auth_host: used internally
          host: used internally
          secret_key: developer secret key, see https://app.bearer.sh/settings
          http_client_settings: Dictionary passed as kwargs to requests.request method
          auth_id: auth id used to connect
          setup_id: the setup id used to store the credentials
        """
        self.integration_id = integration_id
        self.auth_host = auth_host
        self.host = host
        self.secret_key = secret_key
        self.auth_id = auth_id
        self.setup_id = setup_id
        self.http_client_settings = http_client_settings

    def auth(self, auth_id: str):
        """Returns a new integration client instance that will use the given auth id for requests

        Args:
          auth_id: the auth id used to connect
        """
        return Integration(integration_id=self.integration_id,
                           auth_host=self.auth_host,
                           host=self.host,
                           secret_key=self.secret_key,
                           http_client_settings=self.http_client_settings,
                           auth_id=auth_id,
                           setup_id=self.setup_id)

    def authenticate(self, auth_id: str):
        """An alias for `self.auth`
        """
        return self.auth(auth_id)

    def setup(self, setup_id: str):
        """Returns a new integration client instance that will use the given setup id for requests
        Args:
          setup_id: the setup id from the dashboard
        """
        return Integration(integration_id=self.integration_id,
                           auth_host=self.auth_host,
                           host=self.host,
                           secret_key=self.secret_key,
                           http_client_settings=self.http_client_settings,
                           auth_id=self.auth_id,
                           setup_id=setup_id)

    def get_auth(self):
        """Retrieves the auth information (eg. access token) for the current identity.

        You must call `auth` prior to calling this function.
        """
        if self.auth_id is None:
            raise MissingAuthId()

        headers = {
            'Authorization': self.secret_key,
            'User-Agent': self._user_agent(),
            'Content-Type': 'application/json'
        }

        url = f'{self.auth_host}/apis/{self.integration_id}/auth/{self.auth_id}'
        response = requests.get(url, headers=headers, **self.http_client_settings)

        return AuthDetails(response.json())

    def get(self,
            endpoint: str,
            headers: Optional[dict] = None,
            body: Optional[BodyData] = None,
            query: Optional[dict] = None):
        """Makes a GET request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('GET', endpoint, headers, body, query)

    def head(self,
             endpoint: str,
             headers: Optional[dict] = None,
             body: Optional[BodyData] = None,
             query: Optional[dict] = None):
        """Makes a HEAD request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('HEAD', endpoint, headers, body, query)

    def post(self,
             endpoint: str,
             headers: Optional[dict] = None,
             body: Optional[BodyData] = None,
             query: Optional[dict] = None):
        """Makes a POST request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('POST', endpoint, headers, body, query)

    def put(self,
            endpoint: str,
            headers: Optional[dict] = None,
            body: Optional[BodyData] = None,
            query: Optional[dict] = None):
        """Makes a PUT request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('PUT', endpoint, headers, body, query)

    def patch(self,
              endpoint: str,
              headers: Optional[dict] = None,
              body: Optional[BodyData] = None,
              query: Optional[dict] = None):
        """Makes a PATCH request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('PATCH', endpoint, headers, body, query)

    def delete(self,
               endpoint: str,
               headers: Optional[dict] = None,
               body: Optional[BodyData] = None,
               query: Optional[dict] = None):
        """Makes a DELETE request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('DELETE', endpoint, headers, body, query)

    def request(self,
                method: str,
                endpoint: str,
                headers: Optional[dict] = None,
                body: Optional[BodyData] = None,
                query: Optional[dict] = None):
        """Makes a request to the API configured for this integration and returns the response

        Args:
          method: GET/HEAD/POST/PUT/PATCH/DELETE
          endpoint: the URL relative to the configured API's base URL
          headers: any headers to send to the API
          body: any request body data to send
          query: parameters to add to the URL's query string
        """

        s = requests.Session()

        retries = Retry(total=DEFAULT_RETRY,
                        backoff_factor=0.5,
                        status_forcelist=[502, 503, 504])

        s.mount('https://', HTTPAdapter(max_retries=retries))

        pre_headers = {
            'Authorization': self.secret_key,
            'User-Agent': self._user_agent(),
            'Bearer-Auth-Id': self.auth_id,
            'Bearer-Setup-Id': self.setup_id
        }

        if headers is not None:
            request_headers = {**pre_headers, **headers}
        else:
            request_headers = pre_headers

        request_headers = {
            k: v
            for k, v in request_headers.items() if v is not None
        }

        url = '{}/{}/{}'.format(self.host, self.integration_id,
                                endpoint.lstrip('/'))

        self.debug_request(url=url,
                           method=method,
                           body=body,
                           params=query,
                           headers=request_headers,
                           http_client_settings=self.http_client_settings)

        print(f"SENDING REQUEST: {method}, {url}, {query}")
        response = s.request(method,
                             url,
                             headers=request_headers,
                             json=body,
                             params=query,
                             **self.http_client_settings)

        self.info_request(response)
        return response

    def debug_request(self,
                      url=None,
                      method=None,
                      body=None,
                      params=None,
                      headers=None,
                      http_client_settings=None):
        if logger.isEnabledFor(DEBUG):
            logger.debug(
                dedent("""
                sending request
                    url: {}
                    method: {}
                    params: {}
                    body: {}
                    headers: {}
                    http_client_settings: {}

            """.format(url, method, params, body, headers,
                       http_client_settings)).strip())

    def info_request(self, response):
        if logger.isEnabledFor(INFO):
            try:
                requestId = response.headers["Bearer-Request-Id"]
            except KeyError:
                requestId = None
            logger.info(f"request id: {requestId}")

    def _user_agent(self):
        version = pkg_resources.require("bearer")[0].version
        return f'Bearer-Python ({version})'
