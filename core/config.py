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

    @property
    def vault_token(self):
        return self._vault_token

    @property
    def vault_entry_location(self):
        return self._vault_entry_location

    def _get_config(self):
        try:
            config_env_vars = _ConfigEnvVars()
        except EnvironmentError as env_error:
            config_env_vars = None
            print("Unavailable Environment Variables: {}".format(env_error))

        try:
            config_file = _ConfigFile()
        except UnreadableFile as unread_file:
            config_file = None
            print("Configuration file is unreadable: {}".format(unread_file))
        except FileNotFoundError as file_nf:
            config_file = None
            print("Configuration file not exists: {}".format(file_nf))

        if config_env_vars:
            config_source = config_env_vars.config_params
        elif config_file:
            config_source = config_file.config_params
        else:
            raise ConfigurationUnavaliable("Configuration unavaliable: Environment Variables and Configuration File")

        self._vault_url = self._get_config_attribute(
            config_dict=config_source,
            parameter='url'
        )
        self._vault_token = self._get_config_attribute(
            config_dict=config_source,
            parameter='token'
        )
        self._vault_entry_location = self._get_config_attribute(
            config_dict=config_source,
            parameter='entry_location'
        )

    def _get_config_attribute(self, config_dict, parameter, section='vault'):
        for config in config_dict['configurations']:
            if config['section'] == section:
                for param in config['parameters']:
                    if param['property'] == parameter:
                        return param['value']
        return None

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

    @property
    def config_params(self):
        return self._config_params

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

class ConfigurationUnavaliable(Exception):
    pass