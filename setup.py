#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name="zakupkiClient",
      version='1.1.0',
      description='zakupki client',
      url="https://github.com/andreisaw/zakupki",
      long_description=open('README.md').read(),
      author='Andrey',
      author_email='isaevnextdoor@gmail.com',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      install_requires=requirements
      )
