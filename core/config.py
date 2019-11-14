import yaml
import os

class Config:

    def __init__(self):
        self._file_path = self._check_file_exists()
        self._parameteres = dict()

    @property
    def file_path(self):
        return self._file_path

    @property
    def parameters(self):
        return self._parameteres

    def _check_file_exists(self):
        current_directory = os.path.realpath(__file__)
        file_name_accepted = ['config.yml', 'config.yaml']

        for item in os.listdir(current_directory):
            if os.path.isfile(item) and os.access(item, os.R_OK):
                if item in file_name_accepted:
                    return item

        return None