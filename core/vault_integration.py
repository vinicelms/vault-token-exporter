import requests
from config import Config


class Vault:

    def __init__(self):
        self._vault_url = None
        self._vault_token = None
        self._vault_entry_location = None
        self._vault_secret_name = None
        self._get_vault_config()

    @property
    def vault_url(self):
        return self._vault_url

    @property
    def vault_entry_location(self):
        return self._vault_entry_location

    @property
    def vault_secret_name(self):
        return self._vault_secret_name

    def _get_vault_config(self):
        conf = Config()
        self._vault_url = conf.vault_url
        self._vault_token = conf.vault_token
        self._vault_entry_location = conf.vault_entry_location
        self._vault_secret_name = self._vault_entry_location.split('/')[0]