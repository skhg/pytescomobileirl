#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytescomobileirl',
    version='0.0.0',
    description="Unofficial Python Tesco Mobile (Ireland) API",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3.6'])
