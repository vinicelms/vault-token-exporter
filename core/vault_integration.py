import requests
import json
import logging
from config import Config

class Vault:

    def __init__(self):
        self._vault_url = None
        self.__vault_token = None
        self._vault_entry_location = None
        self._vault_secret_name = None
        self._entry_map_name = None
        self._entry_map_token = None
        self.__get_vault_config()

    @property
    def vault_url(self):
        return self._vault_url

    @property
    def vault_entry_location(self):
        return self._vault_entry_location

    @property
    def vault_secret_name(self):
        return self._vault_secret_name

    def __get_vault_config(self):
        conf = Config()
        self._vault_url = conf.vault_url
        self.__vault_token = conf.vault_token
        self._vault_entry_location = conf.vault_entry_location
        self._vault_secret_name = self._vault_entry_location.split('/')[0]
        if len(self._vault_entry_location.split('/')) < 2:
            raise ReferenceError("Entry Location must have at least 2 structures")
        self._entry_map_name = conf.vault_entry_map_name
        self._entry_map_token = conf.vault_entry_map_token

    def __get_list_keys(self):
        request_headers = {"X-Vault-Token" : self.__vault_token}
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

    def __get_key_info(self, entry_key):
        request_headers = {"X-Vault-Token" : self.__vault_token}
        entry_location = self.vault_entry_location.split('/')[1:]
        entry_location = '/'.join(entry_location)
        call_url = "{}/v1/{}/data/{}/{}".format(
            self.vault_url,
            self.vault_secret_name,
            entry_location,
            entry_key
        )
        data_dict = {}
        req = requests.get(call_url, headers=request_headers)
        if req.status_code == 200:
            request_content = json.loads(req.content.decode('utf-8'))
            if 'data' in request_content and 'data' in request_content['data']:
                data_dict = {
                    'token' : request_content['data']['data'][self._entry_map_token]
                }
                if self._entry_map_name:
                    data_dict['name'] = request_content['data']['data'][self._entry_map_name]
                return data_dict
            else:
                raise ReferenceError("Key data unavailable")
        else:
            req.raise_for_status()

    def __get_token_info(self, token, data_content):
        request_headers = {"X-Vault-Token" : self.__vault_token}
        payload = {'token' : token}
        call_url = "{}/v1/auth/token/lookup".format(self.vault_url)
        req = requests.post(call_url, headers=request_headers, data=json.dumps(payload))
        if req.status_code == 200:
            request_content = json.loads(req.content.decode('utf-8'))
            if 'data' in request_content and data_content in request_content['data']:
                return request_content['data'][data_content]
            else:
                raise ReferenceError("Key {} unavailable".format(data_content))
        else:
            req.raise_for_status()

    def get_key_data_from_vault(self):
        key_data_list = []
        try:
            key_list = self.__get_list_keys()
        except EntryKeyUnlistable as eku:
            logging.error(eku)
        except Exception as e:
            logging.exception(e)

        for key in key_list:
            try:
                vault_info = _VaultKeyInfo()
                key_info = self.__get_key_info(entry_key=key)
                vault_info.set_token(key_info['token'])
                vault_info.expiration_time = self.__get_token_info(
                    token=key_info['token'], data_content='ttl'
                )
                vault_info.expiration_time = vault_info.expiration_time / 60
                if 'name' in key_info:
                    vault_info.name = key_info['name']
                else:
                    vault_info.name = self.__get_token_info(
                        token=key_info['token'], data_content='display_name'
                    )
                key_data_list.append(vault_info)
            except ReferenceError as re:
                logging.error(re)
            except Exception as e:
                logging.error("Error collecting information from entry key: \"{}\"\n{}".format(key, e))

        return key_data_list

class _VaultKeyInfo:

    def __init__(self):
        self.name = None
        self.__token = None
        self.expiration_time = None

    def set_token(self, value):
        self.__token = value

class EntryKeyUnlistable(Exception):
    pass