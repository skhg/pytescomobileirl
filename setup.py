#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='pytescomobileirl',
    version='0.2.3',
    description='Unofficial Python Tesco Mobile (Ireland) API',
    long_description='See project page with usage examples at https://github.com/skhg/pytescomobileirl',
    keywords='tesco mobile phone balance status web ireland api',
    author='Jack Higgins',
    author_email='pypi@jackhiggins.ie',
    url='https://github.com/skhg/pytescomobileirl',
    packages=['pytescomobileirl'],
    install_requires=[
        'requests'
    ],
    tests_require=[
        'mock',
        'nose'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ])
