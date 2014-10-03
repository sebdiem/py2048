#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'py2048 is a clone of 2048 in python, playing from the command line',
    'author': 'Sébastien Diemer',
    'url': '',
    'download_url': '',
    'author_email': 'diemersebastien@yahoo.fr',
    'version': '0.1',
    'install_requires': [],
    'packages': ['py2048'],
    'scripts': [],
    'name': 'py2048'
}

setup(**config)
