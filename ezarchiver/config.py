#!env/bin/python

from os.path import join, abspath
import yaml


class Config(object):

    DEFAULT_CONFIG_FILE = 'Archivefile'

    def __init__(self, config_path=None):
        self.config, self.config_file_path = self._load_config(config_path)

    def __str__(self):
        return 'Config: ' + str(self.config)

    @property
    def include(self):
        return self.config.get('include', [])

    @property
    def exclude(self):
        return self.config.get('exclude', [])

    @property
    def root(self):
        return self.config.get('root')

    @property
    def b2(self):
        return self.config['b2']

    @property
    def gpg_key_id(self):
        return self.config['encrypt_key']

    @staticmethod
    def _load_config(config_path):
        from os.path import abspath, dirname, exists, isdir

        config_file_path = None
        loading_from_dir = None
        if isdir(config_path):
            config_file_path = join(config_path, 'Archivefile')
            loading_from_dir = True
        else:
            config_file_path = config_path
            loading_from_dir = False

        if not exists(config_file_path):
            raise ValueError('Config file {} does not exist.'.format(config_file_path))

        with open(config_file_path, 'r') as f:
            config = yaml.safe_load(f)
            if loading_from_dir and 'root' in config:
                raise ValueError(
                    'Explicit root directory in config loaded from directory. '
                    'Root should be determined from {default} location, not provided explicitly. '
                    'Remove root entry from {file}.'.format(default=Config.DEFAULT_CONFIG_FILE, file=config_file_path)
                )
            if 'root' not in config:
                config['root'] = abspath(dirname(config_file_path))

        return config, config_file_path
