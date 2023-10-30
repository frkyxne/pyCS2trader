import os


class ConfigLoader:
    def __init__(self):
        self.__cs_market_api_key = None
        self.__buff_session = None
        self.__request_timeout_min = None
        self.__request_timeout_max = None
        self.__scanned_pages_to_autosave = None
        self.__rub_to_cny_ratio = None
        self.load()

    @property
    def cs_market_api_key(self):
        return self.__cs_market_api_key

    @property
    def buff_session(self):
        return self.__buff_session

    @property
    def request_timeout_min(self):
        return self.__request_timeout_min

    @property
    def request_timeout_max(self):
        return self.__request_timeout_max

    @property
    def scanned_pages_to_autosave(self):
        return self.__scanned_pages_to_autosave

    @property
    def rub_to_cny_ratio(self):
        return self.__rub_to_cny_ratio

    def load(self):
        loader_path = os.path.realpath('__file__')
        s = loader_path.split('\\')
        config_path = loader_path.replace(f'{s[-1]}', '') + 'config.txt'

        try:
            config_lines = open(config_path, 'r').readlines()
        except FileNotFoundError as exception:
            raise ConfigException(f'Config file not found: {exception}')

        try:
            self.__cs_market_api_key = config_lines[0].split()[1]
            self.__buff_session = config_lines[1].split()[1]
            self.__request_timeout_min = int(config_lines[2].split()[1])
            self.__request_timeout_max = int(config_lines[3].split()[1])
            self.__scanned_pages_to_autosave = int(config_lines[4].split()[1])
            self.__rub_to_cny_ratio = int(config_lines[5].split()[1])
        except (ValueError, IndexError) as exception:
            raise ConfigException(f'Invalid config syntax: {exception}')


class ConfigException(Exception):
    pass
