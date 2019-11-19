import requests
import json
from config import Config

class Vault:

    def __init__(self):
        self._vault_url = None
        self._vault_token = None
        self._vault_entry_location = None
        self._vault_secret_name = None
        self._entry_map_name = None
        self._entry_map_token = None
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
        if len(self._vault_entry_location.split('/')) < 2:
            raise ReferenceError("Entry Location must have at least 2 structures")
        self._entry_map_name = conf.vault_entry_map_name
        self._entry_map_token = conf.vault_entry_map_token

    def _get_list_keys(self):
        request_headers = {"X-Vault-Token" : self._vault_token}
        entry_to_list = self.vault_entry_location.split('/')[1:]
        entry_to_list = '/'.join(entry_to_list)
        call_url = "{}/v1/{}/metadata/{}".format(
            self.vault_url,
            self.vault_secret_name,
            entry_to_list
        )
        req = requests.request('LIST', call_url, headers=request_headers)
        if req.status_code == 200:
            request_content = req.json()
            if 'data' in request_content and 'keys' in request_content['data']:
                return request_content['data']['keys']
            else:
                raise ReferenceError("Key list unavailable")
        elif req.status_code == 404:
            raise EntryKeyUnlistable("Entry Key \"{}\" unlistable".format(entry_to_list))
        else:
            req.raise_for_status()

class EntryKeyUnlistable(Exception):
    pass