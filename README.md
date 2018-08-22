# pyfn
[![GitHub release][release-image]][release-url]
[![PyPI release][pypi-image]][pypi-url]
[![Build][build-image]][build-url]
[![Requirements Status][req-image]][req-url]
[![Code Coverage][coverage-image]][coverage-url]
[![FrameNet][framenet-image]][framenet-url]
[![MIT License][license-image]][license-url]

Welcome to **pyfn**, a Python modules to process FrameNet annotation.

pyfn can be used to convert data to and from:
- FRAMENET XML: the format of the released FrameNet XML data
- SEMEVAL XML: the format of the SEMEVAL 2007 shared task 19 on frame semantic structure extraction
- SEMAFOR CoNLL: the format used by the SEMAFOR parser
- BIOS: the format used by the OPEN-SESAME parser

As well as to generate the `.csv` hierarchy files used by both SEMAFOR and
OPEN-SESAME parsers to integrate the hierarchy feature (see (Kshirsagar et al., 2015) for details).

This repository also accompanies the (Kabbach et al., 2018) paper:

```tex
@InProceedings{C18-1267,
  author = 	"Kabbach, Alexandre
		and Ribeyre, Corentin
		and Herbelot, Aur{\'e}lie",
  title = 	"Butterfly Effects in Frame Semantic Parsing: impact of data processing on model ranking",
  booktitle = 	"Proceedings of the 27th International Conference on Computational Linguistics",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"3158--3169",
  location = 	"Santa Fe, New Mexico, USA",
  url = 	"http://aclweb.org/anthology/C18-1267"
}
```

To use pyfn to replicate frame semantic parsing results for SEMAFOR,
OPEN-SESAME and SIMPLEFRAMEID on a common preprocessing pipeline,
or to replicate results reported in (Kabbach et al., 2018),
check out [REPLICATION.md](REPLICATION.md).

## Dependencies
On Unix, you may need to install the following packages:
```
libxml2 libxml2-dev libxslt1-dev
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

For details on `pyfn` usage, do:
```bash
pyfn --help
pyfn generate --help
pyfn convert --help
```

### From FN XML to BIOS
To convert data from FrameNet XML format to BIOS format, do:

```bash
pyfn convert \
  --from fnxml \
  --to bios \
  --source /abs/path/to/fndata-1.x \
  --target /abs/path/to/xp/data/output/dir \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```
Using `--filter overlap_fes` will skip all annotationsets with overlapping
frame elements, as those cases are not supported in the BIOS format.


### From FN XML to SEMAFOR CoNLL
To generate the `train.frame.elements` file used to train SEMAFOR, and the
`{dev,test}.frames` used for decoding, do:

```bash
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /abs/path/to/fndata-1.x \
  --target /abs/path/to/xp/data/output/dir \
  --splits train \
  --output_sentences
```

### From FN XML to SEMEVAL XML
To generate the `{dev,test}.gold.xml` gold files in SEMEVAL format for scoring, do:

```bash
pyfn convert \
  --from fnxml \
  --to semeval \
  --source /abs/path/to/fndata-1.x \
  --target /abs/path/to/xp/data/output/dir \
  --splits {dev,test}
```

### From BIOS to SEMEVAL XML
To convert the decoded BIOS files `{dev,test}.bios.semeval.decoded` of
OPEN-SESAME to SEMEVAL XML format for scoring, do:

```bash
pyfn convert \
  --from bios \
  --to semeval \
  --source /abs/path/to/{dev,test}.bios.semeval.decoded \
  --target /abs/path/to/output/{dev,test}.predicted.xml \
  --sent /abs/path/to/{dev,test}.sentences
```

### From SEMAFOR CoNLL to SEMEVAL XML
To convert the decoded `{dev,test}.frame.elements` files of SEMAFOR to
SEMEVAL XML format for scoring, do:

```bash
pyfn convert \
  --from semafor \
  --to semeval \
  --source /abs/path/to/{dev,test}.frame.elements \
  --target /abs/path/to/output/{dev,test}.predicted.xml \
  --sent /abs/path/to/{dev,test}.sentences
```

### Generate the hierarchy `.csv` files
```bash
pyfn generate \
  --source /abs/path/to/fndata-1.x \
  --target /abs/path/to/xp/data/output/dir
```
To also process exemplars, add the `--with_exemplars` option

[release-image]:https://img.shields.io/github/release/akb89/pyfn.svg?style=flat-square
[release-url]:https://github.com/akb89/pyfn/releases/latest
[pypi-image]:https://img.shields.io/pypi/v/pyfn.svg?style=flat-square
[pypi-url]:https://github.com/akb89/pyfn/releases/latest
[build-image]:https://img.shields.io/travis/akb89/pyfn.svg?style=flat-square
[build-url]:https://gitlab.com/akb89/pyfn/commits/master
[coverage-image]:https://img.shields.io/coveralls/akb89/pyfn/master.svg?style=flat-square
[coverage-url]:https://coveralls.io/github/akb89/pyfn?branch=master
[framenet-image]:https://img.shields.io/badge/framenet-1.5%E2%87%A1-blue.svg?style=flat-square
[framenet-url]:https://framenet.icsi.berkeley.edu/fndrupal
[license-image]:http://img.shields.io/badge/license-MIT-000000.svg?style=flat-square
[license-url]:LICENSE.txt
[req-url]:https://requires.io/github/akb89/pyfn/requirements/?branch=master
[req-image]:https://img.shields.io/requires/github/akb89/pyfn.svg?style=flat-square
