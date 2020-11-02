#!/usr/bin/env python3
"""pyfn setup.py.

This file details modalities for packaging the pyfn application.
"""

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pyfn',
    description='A python module to process data for Frame Semantic Parsing',
    author='Alexandre Kabbach',
    author_email='akb@3azouz.net',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.3.11',
    url='https://gitlab.com/akb89/pyfn',
    download_url='https://pypi.org/project/pyfn/#files',
    license='MIT',
    keywords=['framenet', 'xml', 'frame semantic parsing', 'preprocessing',
              'coling2018', 'pipeline', 'semafor', 'open-sesame'],
    platforms=['any'],
    packages=['pyfn',
              'pyfn.exceptions',
              'pyfn.loading',
              'pyfn.marshalling',
              'pyfn.marshalling.marshallers',
              'pyfn.marshalling.unmarshallers',
              'pyfn.models',
              'pyfn.utils'],
    package_data={'pyfn': ['logging/*.yml']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyfn = pyfn.main:main'
        ],
    },
    install_requires=['pyyaml>=4.2b1', 'mmh3>=2.5.1', 'lxml>=4.3.0',
                      'pytz>=2018.7'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Text Processing :: Linguistic'],
    zip_safe=True,
)
