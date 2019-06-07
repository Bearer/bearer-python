import requests

PRODUCTION_INTEGRATION_HOST = 'https://int.bearer.sh'
FUNCTIONS_PATH = 'api/v4/functions/backend'

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
        headers = { 'Authorization': self.api_key }
        url = '{}/{}/{}/{}'.format(self.integration_host, FUNCTIONS_PATH,  integration_buid, function_name)

        response = requests.post(url, headers=headers, data=body, params=params).json()
        if 'error' in response:
            raise FunctionError(response['error'])
        return response
