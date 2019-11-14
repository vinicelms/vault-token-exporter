import yaml
import os

class Config:

    def __init__(self):
        self._vault_url = None
        self._vault_token = None

    @property
    def vault_url(self):
        return self._vault_url

    @vault_url.setter
    def vault_url(self, value):
        self._vault_url = value

    @property
    def vault_token(self):
        return self._vault_token

    @vault_token.setter
    def vault_token(self, value):
        self._vault_token = value