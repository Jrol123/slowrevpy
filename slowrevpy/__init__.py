from configparser import ConfigParser
from slowrevpy.__main__ import main_processing

config = ConfigParser()
config.read('conf.ini')

__all__ = ["main_processing"]

#! Нужно каким-то образом считывать config файл
# __version__ = config['build_info']['VERSION']
# __author__ = config['package_info']['AUTHORS']
