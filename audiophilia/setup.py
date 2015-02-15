#!/usr/bin/python

import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'audiophilia',
    version = "0.0.1",
    author = 'Daniel Saltiel, Shomik Chakravarty',
    description='Audio analyzer',
    url='https://github.com/drsaltiel/audiophilia',
    packages=['reader','analyzer'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
)


