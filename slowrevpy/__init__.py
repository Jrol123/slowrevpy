from configparser import ConfigParser
from slowrevpy.__main__ import main_processing
from slowrevpy.slowrevpy import slowrevpy

config = ConfigParser()
config.read('conf.ini')

__all__ = ["main_processing", "slowrevpy"]

#! Нужно каким-то образом считывать config файл
# __version__ = config['build_info']['VERSION']
# __author__ = config['package_info']['AUTHORS']
