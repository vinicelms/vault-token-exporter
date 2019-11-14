import yaml
import os
import configparser

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

class _ConfigFile(Config):

    def __init__(self):
        super(_ConfigFile, self).__init__()
        self._file_path = self._get_file_path()
        self._get_config()

    @property
    def vault_url(self):
        return super().vault_url

    @vault_url.setter
    def vault_url(self, value):
        super(_ConfigFile, self.__class__).vault_url.fset(self, value)

    @property
    def vault_token(self):
        return super().vault_token

    @vault_token.setter
    def vault_token(self, value):
        super(_ConfigFile, self.__class__).vault_token.fset(self, value)

    def _get_file_path(self):
        current_directory = os.path.dirname(__file__)
        filename = 'config.ini'
        file_path = "{}{}{}".format(current_directory, os.path.sep, filename)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            if os.access(file_path, os.R_OK):
                return file_path
            else:
                raise UnreadableFile("File unreadable: {}".format(file_path))
        else:
            raise FileNotFoundError("File not exists: {}".format(file_path))

    def _get_config(self):
        config = configparser.ConfigParser()
        config.read(self._file_path)
        if 'vault' in config.sections():
            if 'url' in config['vault']:
                self.vault_url = config['vault']['url']
            else:
                raise ValueError("Vault URL not defined in configuration file")

            if 'token' in config['vault']:
                self.vault_token = config['vault']['token']
            else:
                raise ValueError("Vault Token not defined")
        else:
            raise ValueError("Vault section not defined")

class UnreadableFile(Exception):
    pass