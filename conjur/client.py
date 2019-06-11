from .api import Api
from .config import Config
import os

class Client():
    def __init__(self, appliance_url=None, cert_file=None, account=None, username=None, password=None, ssl_verify=True):
        self.config = Config()
        self.config.load(appliance_url, cert_file, account, username, password, ssl_verify)
        self.api = Api(self.config)

    def authenticate(self):
        return self.api.authenticate()

    def retrieve_secret(self, identifier, kind="variable"):
        return self.api.retrieve_secret(identifier, kind)

    def list_resources(self):
        return self.api.list_resources()

    def list_resources_simple(self):
        resources = self.list_resources()
        ids = []
        for resource in resources:
            ids.append(resource['id'])
        return ids

