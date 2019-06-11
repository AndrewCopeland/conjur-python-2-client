from yaml import load, Loader
import os
import netrc
import sys

class ConfigError(Exception):
    pass

class Config():
    def load(self, appliance_url, cert_file, account, username, password, verify_ssl):
        # retrieve info from ~/.conjurrc
        if appliance_url is None or cert_file is None or account is None:
            conjurrc_path = os.path.expanduser("~/.conjurrc")
            config = None
            try:
                with open(conjurrc_path, 'r') as config_fp:
                    config = load(config_fp, Loader=Loader)
                    self.account = config['account']
                    self.cert_file = config['cert_file']
                    self.appliance_url = config['appliance_url']
            except Exception:
                raise ConfigError("Conjur file '{}' does not exists or cannot be read".format(conjurrc_path)), None, sys.exc_info()[2]
        else:
            self.account = account
            self.cert_file = cert_file
            self.appliance_url = appliance_url

        # retrieve from ~/.netrc
        if username is None or password is None:
            netrc_path = os.path.expanduser("~/.netrc")
            netrc_file = None
            try:
                netrc_file = netrc.netrc(netrc_path)
                self.username, _, self.password = netrc_file.authenticators(netrc_file.hosts.keys().pop())
            except Exception:
                raise ConfigError("Conjur file '{}' does not exists or cannot be read".format(netrc_path)), None, sys.exc_info()[2]
        else:
            self.username = username
            self.password = password

        if verify_ssl is None:
            verify_ssl = False
        self.verify_ssl = verify_ssl

        if cert_file:
            self.verify_ssl = cert_file

 
            

        
                


            

