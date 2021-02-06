import requests


class Connector:

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def get_json(self):
        response = requests.get(url=self.url, params=self.params)
        response.raise_for_status()
        return response.json()
