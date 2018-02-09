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
    install_requires=['PyYAML==3.12', 'mmh3==2.4', 'lxml==3.7.3'],
    setup_requires=['pytest-runner==3.0', 'pytest-pylint==0.8.0'],
    tests_require=['pytest==3.4.0', 'pylint==1.8.2'],
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
