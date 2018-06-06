# pyfn
[![PyPI release][pypi-image]][pypi-url]
[![Build][build-image]][build-url]
[![FrameNet][framenet-image]][framenet-url]
[![MIT License][license-image]][license-url]

Welcome to **pyfn**, a Python modules to process FrameNet annotation.

pyfn can be used to convert data to and from:
- FrameNet XML: the format of the released FrameNet data
- Semeval XML: the format of the SEMEVAL 2007 shared task 19 on frame semantic structure extraction
- CoNLL: the format used by the SEMAFOR parser
- BIOS: the format used by the OPEN-SESAME parser

This repository also accompanies the Kabbach et al. (2018) paper
*Butterfly Effects in Frame Semantic Parsing: impact of data processing on model ranking*
```tex

```

To use pyfn to replicate frame semantic parsing results for SEMAFOR,
OPEN-SESAME and SIMPLEFRAMEID on a common preprocessing pipeline,
or to replicate results reported in Kabbach et al. (2018),
check out [REPLICATION.md](REPLICATION.md).

## Dependencies
On Unix, you may need to install the following packages:
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

## Formats
For an exhaustive description of all formats, check out [FORMAT.md](FORMAT.md).

## Conversion HowTo
The following sections provide examples of commands to convert FN data
to and from different formats. All commands can make use of the following options:
1. `--splits`: specify which splits should be converted. Use `--splits dev`
to only process dev and test splits and guarantee no overlap between
dev and test. Use `--splits train` to process train dev and test splits and
guarantee no overlap across splits. Default to `--splits test`.
2. `--output_sentences`: if specified, will output a `.sentences` file
in the process, containing all raw annotated sentences, one sentence per line.
3. `--with_exemplars`: if specified, will process the exemplars (data under
the `lu` directory) in addition to fulltext.
4. `--filter`: specify data filtering options (see details below).

### From FN XML to BIOS
To convert data from FrameNet XML format to BIOS format:
```bash
pyfn convert \
  --from fnxml \
  --to bios \
  --source /abs/path/to/fndata-1.x \
  --target /abs/path/to/output/dir \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```
Using `--filter overlap_fes` will skip all annotationsets with overlapping
frame elements, as those cases are not supported in the BIOS format.


### From FN XML to CoNLL
```bash
pyfn --from fnxml --to conll --source /abs/path/to/fndata-1.x --target /abs/path/to/output/dir
```

### From FN XML to SEMEVAL XML
To generate a `test.gold.xml` file in SEMEVAL format:
```bash
pyfn --from fnxml --to semeval --source /abs/path/to/fndata-1.x --target /abs/path/to/output/dir --splits test
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
[build-image]:https://img.shields.io/travis/akb89/pyfn.svg?style=flat-square
[build-url]:https://gitlab.unige.ch/akb/pyfn/commits/master
[coverage-image]:https://img.shields.io/coveralls/akb89/pyfn/master.svg?style=flat-square
[coverage-url]:https://coveralls.io/github/akb89/pyfn?branch=master
[framenet-image]:https://img.shields.io/badge/framenet-1.5%E2%87%A1-blue.svg?style=flat-square
[framenet-url]:https://framenet.icsi.berkeley.edu/fndrupal
[license-image]:http://img.shields.io/badge/license-MIT-000000.svg?style=flat-square
[license-url]:LICENSE.txt
[req-url]:https://requires.io/github/akb89/pyfn/requirements/?branch=master
[req-image]:https://img.shields.io/requires/github/akb89/pyfn.svg?style=flat-square
