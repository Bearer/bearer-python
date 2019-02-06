import requests

INT_URL = 'https://int.bearer.sh/api/v2/intents/backend/'


class Client():
    """Bearer http client"""

    def __init__(self, token: str):
        self.token = token

    def call(self, integrationId: str, intentName: str, options: object = {}):
        headers = {'Authorization': self.token}
        response = requests.post(
            INT_URL + integrationId + '/' + intentName, headers=headers, data=options)
        print('Data sent: {!r}'.format(response.json()))


c = Client('HExbb3Tvba2hLl-VBBWKVO-sUUzpLYD-')
c.call("9eabba-github-actions-auto-push", "SpongeBobIsTheKing", {'page': 1})
