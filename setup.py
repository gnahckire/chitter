#!/usr/bin/env python

from distutils.core import setup

setup(name='ciscospark',
      version='0.1.0',
      description='Python wrapper for Cisco Spark API',
      author='Erik Chang',
      author_email='gnahckire@email.com',
      url='',
      packages=['spark'],
      install_requires=['requests']
     )