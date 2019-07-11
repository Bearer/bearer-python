import requests
import warnings

from typing import Optional, Union

PRODUCTION_INTEGRATION_HOST = 'https://int.bearer.sh'
FUNCTIONS_PATH = 'api/v4/functions/backend'
PROXY_FUNCTION_NAME = 'bearer-proxy'

class FunctionError(Exception):
    def __init__(self, response):
      super().__init__(response)
      self.response = response

class Bearer():
    """Bearer client

    Example:
      >>> from bearer import Bearer
      >>>
      >>> bearer = Bearer('<api-key>')
      >>> bearer.invoke('<buid>', 'defaultFunction')
    """

    def __init__(self, api_key: str, integration_host: str = PRODUCTION_INTEGRATION_HOST):
        """
        Args:
          api_key: developer API Key from the Dashboard

        """
        self.api_key = api_key
        self.integration_host = integration_host

    def invoke(self, integration_buid: str, function_name: str, body: dict = {}, params: dict = {}):
        """Invoke an integration function

        Args:
          integration_buid: identifier of the integration
          function_name: function to invoke
          body: data to pass in the body of the request
          params: parameters to pass in the query string of the request

        """
        warnings.warn("Please use integration(...).invoke(...) instead", DeprecationWarning)
        return self.integration(integration_buid).invoke(
            function_name=function_name,
            body=body,
            query=params
        )

    def integration(self, integration_id: str):
        return Integration(integration_id, self.integration_host, self.api_key)

BodyData = Union[dict, list]

class Integration():
    def __init__(
        self,
        integration_id: str,
        integration_host: str,
        api_key: str,
        setup_id: str = None,
        auth_id: str = None
    ):
        self.integration_id = integration_id
        self.integration_host = integration_host
        self.api_key = api_key
        self.setup_id = setup_id
        self.auth_id = auth_id

    def invoke(self, function_name: str, body: dict = {}, query: dict = None):
        """Invoke an integration function

        Args:
          integration_buid: identifier of the integration
          function_name: function to invoke
          body: data to pass in the body of the request
          query: parameters to pass in the query string of the request
        """

        headers = { 'Authorization': self.api_key }
        url = '{}/{}/{}/{}'.format(self.integration_host, FUNCTIONS_PATH, self.integration_id, function_name)

        response = requests.post(url, headers=headers, data=body, params=query).json()
        if 'error' in response:
            raise FunctionError(response['error'])
        return response

    def setup(self, setup_id: str):
        """Returns a new integration client instance that will use the given setup id for requests

        Args:
          setup_id: the setup id from the dashboard
        """
        return Integration(
            self.integration_id,
            self.integration_host,
            self.api_key,
            setup_id,
            self.auth_id
        )

    def auth(self, auth_id: str):
        """Returns a new integration client instance that will use the given auth id for requests

        Args:
          auth_id: the auth id used to connect
        """
        return Integration(
            self.integration_id,
            self.integration_host,
            self.api_key,
            self.setup_id,
            auth_id
        )

    def authenticate(self, auth_id: str):
        """An alias for `self.auth`
        """
        return self.auth(auth_id)

    def get(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a GET request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('GET', endpoint, headers, body, query)

    def head(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a HEAD request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('HEAD', endpoint, headers, body, query)

    def post(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a POST request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('POST', endpoint, headers, body, query)

    def put(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a PUT request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('PUT', endpoint, headers, body, query)

    def patch(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a PATCH request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('PATCH', endpoint, headers, body, query)

    def delete(self, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a DELETE request to the API configured for this integration and returns the response

        See `self.request` for a description of the parameters
        """
        return self.request('DELETE', endpoint, headers, body, query)

    def request(self, method: str, endpoint: str, headers: Optional[dict] = None, body: Optional[BodyData] = None, query: Optional[dict] = None):
        """Makes a request to the API configured for this integration and returns the response

        Args:
          method: GET/HEAD/POST/PUT/PATCH/DELETE
          endpoint: the URL relative to the configured API's base URL
          headers: any headers to send to the API
          body: any request body data to send
          query: parameters to add to the URL's query string
        """

        pre_headers = {
          'Authorization': self.api_key,
          'User-Agent': 'Bearer.sh',
          'Bearer-Auth-Id': self.auth_id,
          'Bearer-Setup-Id': self.setup_id
        }

        if headers is not None:
          for key, value in headers.items():
            pre_headers['Bearer-Proxy-{}'.format(key)] = value

        request_headers = {k: v for k, v in pre_headers.items() if v is not None}
        url = '{}/{}/{}/{}/{}'.format(self.integration_host, FUNCTIONS_PATH, self.integration_id, PROXY_FUNCTION_NAME, endpoint.lstrip('/'))

        return requests.request(method, url, headers=request_headers, json=body, params=query)
