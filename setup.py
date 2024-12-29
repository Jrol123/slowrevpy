from setuptools import setup, find_packages
from configparser import ConfigParser
import codecs
import os

config = ConfigParser()
if not config.read('conf.ini'):
    raise FileNotFoundError("Файл конфигурации 'conf.ini' не найден.")

# Setting up
setup(
    name="slowrevpy",
    version=config['build_info']['VERSION'],
    author="Jrol123",
    author_email="<angap4@gmail.com>",
    description=config['build_info']['DESCRIPTION'],
    packages=find_packages(),
    install_requires=['pedalboard', 'soundfile', 'argparse', 'python-ffmpeg'],
    keywords=['python', 'music', 'slowed reverb', 'Jrol123'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)