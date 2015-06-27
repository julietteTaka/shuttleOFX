#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import os
from setuptools import setup

VERSION = "1.0"

base = os.path.dirname(__file__)
readme = open(os.path.join(base, 'README.md')).read()

setup(
    name='shuttleofx',
    version=VERSION,
    description='ShuttleOFX',
    long_description=readme,
    author='Marc-Antoine ARNAUD',
    author_email='arnaud.marcantoine@gmail.com',
    url='https://github.com/ShuttleOFX/shuttleofx',
    data_files=[
      ('/etc/uwsgi/apps-available', [
        'etc/uwsgi/apps-available/shuttleofx_analyser.ini',
        'etc/uwsgi/apps-available/shuttleofx_catalog.ini',
        'etc/uwsgi/apps-available/shuttleofx_client.ini',
        'etc/uwsgi/apps-available/shuttleofx_render.ini',
        ]),
      ('/etc/nginx/sites-available', [
        'etc/nginx/sites-available/shuttleofx_analyser',
        'etc/nginx/sites-available/shuttleofx_catalog',
        'etc/nginx/sites-available/shuttleofx_client',
        'etc/nginx/sites-available/shuttleofx_render',
        ]),
      ('/var/www/shuttleofx', [
        'var/www/shuttleofx/analyser.py',
        'var/www/shuttleofx/catalog.py',
        'var/www/shuttleofx/client.py',
        'var/www/shuttleofx/render.py',
        ]),
      ('/etc/shuttleofx', [
        'etc/shuttleofx/analyser.cfg',
        'etc/shuttleofx/catalog.cfg',
        'etc/shuttleofx/client.cfg',
        'etc/shuttleofx/render.cfg',
        ]),
    ],
    packages=[
        'shuttleofx_analyser',
        'shuttleofx_catalog',
        'shuttleofx_client',
        'shuttleofx_render',
    ],
    package_data={'shuttleofx_client': [
      'templates/*.html',
      'static_tmp/fonts/*',
      'static_tmp/images/*.*',
      'static_tmp/images/collaborators/*.*',
      'static_tmp/images/features/*.*',
      'static_tmp/images/personae/*.*',
      'static_tmp/images/team/*.*',
      'static_tmp/images/vehier/*.*',
      'static_tmp/scripts/*.*',
      'static_tmp/scripts/vendor/*',
      'static_tmp/styles/*.*',
      'static_tmp/styles/vendor/*',
      'static_tmp/sub/*',
      'Gruntfile.js',
      'package.json',
    ]},
    install_requires=[
        'Flask>=0.8.1',
        'requests>=2.5.1',
        'pymongo>=2.8'
    ],
)
