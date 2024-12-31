from setuptools import setup, find_packages
from configparser import ConfigParser
import codecs
import os

config = ConfigParser()
if not config.read('conf.ini'):
    raise FileNotFoundError("Файл конфигурации 'conf.ini' не найден.")

README_FILENAME = 'README.md'
with open(README_FILENAME, encoding="utf-8") as f:
    long_description = f.read()

# Setting up
setup(
    include_package_data=True,
    name="slowrevpy",
    version=config['build_info']['VERSION'],
    author="Jrol123",
    author_email="<angap4@gmail.com>",
    description=config['package_info']['DESCRIPTION'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=config['package_info']['URL'],
    license=config['package_info']['LICENSE'],
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