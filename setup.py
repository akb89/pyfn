#!/usr/bin/env python3
"""pyFN setup.py.

This file details modalities for packaging the pyFN application

"""

from setuptools import setup

setup(
    name='pyFN',
    description='A python module to process FrameNet XML data ',
    author='Alexandre Kabbach',
    author_email='akb@3azouz.net',
    # version=__import__('pFN').get_version(),
    version='0.1.0',
    url='https://github.com/akb89/pyFN',
    license='MIT',
    platforms=['any'],
    packages=['pyFN'],
    # Add test suite
)
