#!/usr/bin/env python3
"""pyFN setup.py.

This file details modalities for packaging the pyFN application.
"""

from setuptools import setup

setup(
    name='pyFN',
    description='A python module to process FrameNet XML data',
    author='Alexandre Kabbach',
    author_email='akb@3azouz.net',
    version='0.1.0',
    url='https://github.com/akb89/pyFN',
    license='MIT',
    platforms=['any'],
    packages=['pyFN',
              'pyFN.extraction',
              'pyFN.extraction.extractors',
              'pyFN.loading',
              'pyFN.marshalling',
              'pyFN.marshalling.marshallers',
              'pyFN.marshalling.unmarshallers',
              'pyFN.models',
              'pyFN.utils'],
    # Add test suite
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Text Processing :: Linguistic'],
)
