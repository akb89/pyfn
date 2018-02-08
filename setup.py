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
    download_url='https://github.com/akb89/pyFN/archive/0.1.0.tar.gz',
    license='MIT',
    keywords=['framenet', 'xml', 'marshalling', 'unmarshalling'],
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
    install_requires=['pyaml', 'mmh3', 'lxml'],
    setup_requires=['pytest-runner', 'pytest-pylint'],
    tests_require=['pytest', 'pylint'],
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Text Processing :: Linguistic'],
)
