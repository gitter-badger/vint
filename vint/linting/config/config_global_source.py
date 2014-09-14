from pathlib import Path
from vint.linting.config.config_file_source import ConfigFileSource

GLOBAL_CONFIG_FILENAME = '.vintrc.yaml'
VOID_CONFIG_PATH = Path('asset') / 'void_config.yaml'


class ConfigGlobalSource(ConfigFileSource):
    def get_file_path(self, env):
        global_config_path = env['home_path'] / GLOBAL_CONFIG_FILENAME

        if global_config_path.is_file():
            return global_config_path
        else:
            return VOID_CONFIG_PATH
