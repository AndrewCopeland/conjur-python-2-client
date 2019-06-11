import base64
import requests
import urllib
from .config import Config
import json

class ConjurApiError(Exception):
    pass

class Api():

    def __init__(self, config):
        self.config = config
        self.api_key = None
        self.session_token = None
        self.default_headers = {}

        if not self.config.verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def login(self):
        url = "{}/authn/{}/login".format(self.config.appliance_url, self.config.account)
        headers = {"Authorization": "Basic {}".format(base64.b64encode("{}:{}".format(self.config.username, self.config.password)))}
        response = requests.get(url, headers=headers, verify=self.config.verify_ssl)

        if response.status_code != 200:
            raise ConjurApiError("Status code: {}. Failed to login into the conjur api. Response from conjur api '{}'".format(response.status_code, response.text))

        return response.text
    
    def authenticate(self):
        api_key = self.login()
        url = "{}/authn/{}/{}/authenticate".format(self.config.appliance_url, self.config.account, self.config.username)
        response = requests.post(url, data=api_key, verify=self.config.verify_ssl)

        if response.status_code != 200:
            raise ConjurApiError("Status code: {}. Failed to authenticate into the conjur api. Response from conjur api '{}'".format(response.status_code, response.text))

        self.session_token = response.text
        self.default_headers["Authorization"] = 'Token token="{}"'.format(base64.b64encode(self.session_token))

    def retrieve_secret(self, identifier, kind="variable"):
        identifier = urllib.quote(identifier, safe='')
        url = "{}/secrets/{}/{}/{}".format(self.config.appliance_url, self.config.account, kind, identifier)
        response = requests.get(url, headers=self.default_headers, verify=self.config.verify_ssl)

        # Only attempt to authenticate once. This is if the token has expired or was never authenticated.
        if response.status_code == 401:
            self.authenticate()
            return self.retrieve_secret(identifier, kind)

        if response.status_code != 200:
            raise ConjurApiError("Status code: {}. Failed to retrieve secret from the conjur api. Response from conjur api '{}'".format(response.status_code, response.text))

        return response.text

    def list_resources(self):
        url = "{}/resources/{}".format(self.config.appliance_url, self.config.account)
        response = requests.get(url, headers=self.default_headers, verify=self.config.verify_ssl)
        # Only attempt to authenticate once. This is if the token has expired or was never authenticated.
        if response.status_code == 401:
            self.authenticate()
            return self.list_resources()

        if response.status_code != 200:
            raise ConjurApiError("Status code: {}. Failed to list resources from the conjur api. Response from conjur api '{}'".format(response.status_code, response.text))

        return json.loads(response.text, encoding='unicode')



