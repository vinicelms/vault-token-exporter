import yaml
import os
import configparser

class _Config:

    def __init__(self):
        self._vault_url = None
        self._vault_token = None
        self._vault_entry_location = None

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

    @property
    def vault_entry_location(self):
        return self._vault_entry_location

    @vault_entry_location.setter
    def vault_entry_location(self, value):
        self._vault_entry_location = value

class _ConfigFile():

    def __init__(self):
        self._file_path = self._get_file_path()
        self._config_params = self._get_config()

    @property
    def config_params(self):
        return self._config_params

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
        self._config_params = {'configurations' : []}

        section_dict = {}
        for section in config.sections():
            section_dict = {'section' : section, 'parameters' : []}
            for item in config[section]:
                section_dict['parameters'].append({'property' : item, 'value' : config[section][item]})
            self._config_params['configurations'].append(section_dict)

        return self.config_params

class _ConfigEnvVars():

    def __init__(self):
        self._config_params = self._get_environment_variables()

    def _get_environment_variables(self):
        config_dict = {'configurations' : []}
        if 'VAULT_URL' in os.environ:
            vault_section_dict = {'section' : 'vault', 'parameters' : []}
            vault_section_dict['parameters'].append({'url' : os.environ['VAULT_URL']})
        else:
            raise EnvironmentError("VAULT_URL environment variable not defined")

        if 'VAULT_TOKEN' in os.environ:
            vault_section_dict['parameters'].append({'token' : os.environ['VAULT_TOKE']})
        else:
            raise EnvironmentError("VAULT_TOKEN environment variable not defined")

        if 'VAULT_ENTRY_LOCATION' in os.environ:
            vault_section_dict['parameters'].append({'entry_location' : os.environ['VAULT_ENTRY_LOCATION']})
        else:
            raise EnvironmentError("VAULT_ENTRY_LOCATION environment variable not defined")

        config_dict['configurations'].append(vault_section_dict)
        return config_dict

class UnreadableFile(Exception):
    pass