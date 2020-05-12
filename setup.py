#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from codecs import open

from setuptools import setup, find_packages


with open('sqlmapcli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()


setup(
    name='sqlmapcli',
    version=version,
    description='Simplify your operations for sqlmapapi',
    long_description=readme + '\n\n' + history,
    author='jetz',
    author_email='jet.zheung@gmail.com',
    url='https://www.github.com/jetz/sqlmapcli',
    packages=find_packages(),
    install_requires=['requests>=2.10.0'],
    license='MIT',
    keywords='sqlmap, sqlmapapi, sqlmapcli, sqlmap-proxy, sqlmap-client',
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    )
)
