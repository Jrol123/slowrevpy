from configparser import ConfigParser
from slowrevpy.__main__ import main_processing

config = ConfigParser()
config.read('conf.ini')

__all__ = ["main_processing"]
__version__ = "1.5.1"

__author__="Artemii Popovkin"
# GLOBAL_EMAIL=<angap4@gmail.com>
# DESCRIPTION=A basic python script to make slowed + reverbs.
# URL=https://github.com/Jrol123/slowedreverb_main
# LICENSE=MIT

#! Нужно каким-то образом считывать config файл
# __version__ = config['build_info']['VERSION']
# __author__ = config['package_info']['AUTHORS']
