# pyfn
[![GitHub release][release-image]][release-url]
[![PyPI release][pypi-image]][pypi-url]
[![Build][travis-image]][travis-url]
[![Requirements Status][req-image]][req-url]
[![Code Coverage][coverage-image]][coverage-url]
[![FrameNet][framenet-image]][framenet-url]
[![MIT License][license-image]][license-url]

Welcome to **pyfn**, a Python modules to process FrameNet annotation.

pyfn can be used to convert data to and from:
- FrameNet XML: the format of the released FrameNet data
- Semeval XML: the format of the SEMEVAL 2007 shared task 19 on frame semantic structure extraction
- CoNLL: the format used by the SEMAFOR parser
- BIOS: the format used by the OPEN-SESAME parser

To use pyfn to replicate frame semantic parsing results for SEMAFOR,
OPEN-SESAME and SIMPLEFRAMEID on a common preprocessing pipeline,
check out [REPLICATION.md](REPLICATION.md).

## Dependencies
On Linux:
```
sudo apt-get install libxml2 libxml2-dev libxslt1-dev
```

## Install
```
pip3 install pyfn
```

## Use
When using pyfn, your FrameNet splits directory structure should follow:
```
.
|-- fndata-1.x
|   |-- train
|   |   |-- fulltext
|   |   |-- lu
|   |-- dev
|   |   |-- fulltext
|   |   |-- lu
|   |-- test
|   |   |-- fulltext
|   |   |-- lu
```

### From FN XML to BIOS

```bash
pyfn --from fnxml --to bios --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir
```
To add exemplars to fulltext data, do:
```bash
pyfn --from fnxml --to bios --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir --with_exemplars true
```

### From FN XML to CoNLL
```bash
pyfn --from fnxml --to conll --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir
```
To add exemplars to fulltext data, do:
```bash
pyfn --from fnxml --to conll --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir --with_exemplars true
```

### From FN XML to SEMEVAL XML
To generate a `dev.gold.xml` file in SEMEVAL format:
```bash
pyfn --from fnxml --to semeval --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir --splits dev
```
To generate a `test.gold.xml` file in SEMEVAL format:
```bash
pyfn --from fnxml --to semeval --source /abs/path/to/fn/splits/dir --target /abs/path/to/output/dir --splits test
```

### From BIOS to SEMEVAL XML
```bash
pyfn --from bios --to semeval --source /abs/path/to/bios/file --target /abs/path/to/output/dir
```

### From CoNLL to SEMEVAL XML
```bash
pyfn --from conll --to semeval --source /abs/path/to/conll/file --target /abs/path/to/output/dir
```

[release-image]:https://img.shields.io/github/release/akb89/pyfn.svg?style=flat-square
[release-url]:https://github.com/akb89/pyfn/releases/latest
[pypi-image]:https://img.shields.io/pypi/v/pyfn.svg?style=flat-square
[pypi-url]:https://github.com/akb89/pyfn/releases/latest
[travis-image]:https://img.shields.io/travis/akb89/pyfn.svg?style=flat-square
[travis-url]:https://travis-ci.org/akb89/pyfn
[coverage-image]:https://img.shields.io/coveralls/akb89/pyfn/master.svg?style=flat-square
[coverage-url]:https://coveralls.io/github/akb89/pyfn?branch=master
[framenet-image]:https://img.shields.io/badge/framenet-1.5%E2%87%A1-blue.svg?style=flat-square
[framenet-url]:https://framenet.icsi.berkeley.edu/fndrupal
[license-image]:http://img.shields.io/badge/license-MIT-000000.svg?style=flat-square
[license-url]:LICENSE.txt
[req-url]:https://requires.io/github/akb89/pyfn/requirements/?branch=master
[req-image]:https://img.shields.io/requires/github/akb89/pyfn.svg?style=flat-square
