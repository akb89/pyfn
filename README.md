# pyfn
[![GitHub release][release-image]][release-url]
[![PyPI release][pypi-image]][pypi-url]
[![Build][travis-image]][travis-url]
[![Requirements][req-image]][req-url]
[![Code Coverage][coverage-image]][coverage-url]
[![FrameNet][framenet-image]][framenet-url]
[![MIT License][license-image]][license-url]

Welcome to `pyfn`, a Python module to process FrameNet annotation.

`pyfn` can be used to:

1. [convert](#conversion) data to and from FRAMENET XML, SEMEVAL XML, SEMAFOR CoNLL, BIOS and CoNLL-X
2. [preprocess](#preprocessing-and-frame-semantic-parsing) FrameNet data using a standardized state-of-the-art pipeline
3. [run](#preprocessing-and-frame-semantic-parsing) the SEMAFOR,  OPEN-SESAME and SIMPLEFRAMEID frame semantic parsers for frame and/or argument identification on the FrameNet 1.5, 1.6 and 1.7 datasets
4. [build](#marshalling-and-unmarshalling-framenet-xml-data) your own frame semantic parser using a standard set of python models to marshall/unmarshall FrameNet XML data

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

## Dependencies
On Unix, you may need to install the following packages:
```
libxml2 libxml2-dev libxslt1-dev python-3.x-dev
```

## Install
```
pip3 install pyfn
```

## Use
When using `pyfn`, your FrameNet splits directory structure should follow:
```
.
|-- fndata-1.x-with-dev
|   |-- train
|   |   |-- fulltext
|   |   |-- lu
|   |-- dev
|   |   |-- fulltext
|   |   |-- lu
|   |-- test
|   |   |-- fulltext
|   |   |-- lu
|   |-- frame
|   |-- frRelation.xml
|   |-- semTypes.xml
```

## Conversion

`pyfn` can be used to convert data to and from:
- FRAMENET XML: the format of the released FrameNet XML data
- SEMEVAL XML: the format of the SEMEVAL 2007 shared task 19 on frame semantic structure extraction
- SEMAFOR CoNLL: the format used by the SEMAFOR parser
- BIOS: the format used by the OPEN-SESAME parser
- CoNLL-X: the format used by various state-of-the-art POS taggers and dependency
parsers (see preprocessing considerations for frame semantic parsing
[below](#preprocessing-and-frame-semantic-parsing))

As well as to generate the `.csv` hierarchy files used by both SEMAFOR and
OPEN-SESAME parsers to integrate the hierarchy feature (see (Kshirsagar et al., 2015) for details).

For an exhaustive description of all formats, check out [FORMAT.md](FORMAT.md).

### HowTo

The following sections provide examples of commands to convert FN data
to and from different formats. All commands can make use of the following options:
1. `--splits`: specify which splits should be converted. `--splits train` will generate all
train/dev/test splits, according to data found under the fndata-1.x/{train/dev/test}
directories. `--splits dev` will generate the dev and test splits according to data found under
the fndata-1.x/{dev/test} directories. This option will skip the train splits but generate the
same dev/test splits that would have been generated with `--splits train`. `--splits test` will
generate the test splits according to data found under the fndata-1.x/test directory, and skip
the train/dev splits. The test splits generated with `--splits test` will be the same as those
generated with the `--splits train` and `--splits dev`. Default to `--splits test`.
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
frame elements, as those cases are not supported by the BIOS format.


### From FN XML to SEMAFOR CoNLL
To generate the `train.frame.elements` file used to train SEMAFOR, and the
`{dev,test}.frames` file used for decoding, do:

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


## Preprocessing and Frame Semantic Parsing
`pyfn` ships in with a set of bash scripts to preprocess FrameNet data with
various POS taggers and dependency parsers, as well as to perform frame
semantic parsing with a variety of open-source parsers.

Currently supported POS taggers include:
- MXPOST (Ratnaparkhi, 1996)
- NLP4J (Choi, 2016)

Currently supported dependency parsers include:
- MST (McDonald et al., 2006)
- BIST BARCH (Kiperwasser and Goldberg, 2016)
- BIST BMST (Kiperwasser and Goldberg, 2016)

Currently supported frame semantic parsers include:
- SIMPLEFRAMEID (Hartmann et al., 2017) for frame identification
- SEMAFOR (Kshirsagar et al., 2015) for argument identification
- OPEN-SESAME (Swayamdipta et al., 2017) for argument identification

To request support for a POS tagger, a dependency parser or a frame semantic
parser, please create an [issue](https://github.com/akb89/pyfn/issues) on Github/Gitlab.

### Download
To run the preprocessing and frame semantic parsing scripts, first download:
- `data.7z` containing all the FrameNet splits for FN 1.5 and FN 1.7
```shell
wget backup.3azouz.net/pyfn/data.7z
```
- `lib.7z` containing all the different external softwares (taggers, parsers, etc.)
```shell
wget backup.3azouz.net/pyfn/lib.7z
```
- `resources.7z` containing all the required resources
```shell
wget backup.3azouz.net/pyfn/resources.7z
```
- `scripts.7z` containing the set of bash scripts to call the different parsers and preprocessing toolkits
```shell
wget backup.3azouz.net/pyfn/scripts.7z
```

Extract the content of all the archives under a
directory named `pyfn`. Your pyfn folder structure should look like:
```
.
|-- pyfn
|   |-- data
|   |   |-- fndata-1.5-with-dev
|   |   |-- fndata-1.7-with-dev
|   |-- lib
|   |   |-- bistparser
|   |   |-- jmx
|   |   |-- mstparser
|   |   |-- nlp4j
|   |   |-- open-sesame
|   |   |-- semafor
|   |   |-- semeval
|   |-- resources
|   |   |-- bestarchybrid.model
|   |   |-- bestarchybrid.params
|   |   |-- bestfirstorder.model
|   |   |-- bestfirstorder.params
|   |   |-- config-decode-pos.xml
|   |   |-- nlp4j.plemma.model.all.xz
|   |   |-- sskip.100.vectors
|   |   |-- wsj.model
|   |-- scripts
|   |   |-- CoNLLizer.py
|   |   |-- deparse.sh
|   |   |-- flatten.sh
|   |   |-- ...
```

**Please strictly follow this directory structure to avoid unexpected errors. `pyfn` relies on a lot of relative path resolutions to make scripts calls shorter, and changing this directory structure can break everything**

### Setup NLP4J for POS tagging

To use NLP4J for POS tagging, modify the `resources/config-decode-pos.xml`
file by replacing the models.pos absolute path to
your `resources/nlp4j.plemma.model.all.xz`:
```xml
<configuration>
	...
	<models>
		<pos>/absolute/path/to/pyfn/resources/nlp4j.plemma.model.all.xz</pos>
	</models>
</configuration>
```

### Setup DyNET for BIST or OPEN-SESAME

If you intend to use the BIST parser for dependency parsing or
OPEN-SESAME for frame semantic parsing, you will need
to install DyNET 2.0.2 via:
```
pip install dynet=2.0.2
```
If you experience problems installing DyNET via pip, follow:
```
https://dynet.readthedocs.io/en/2.0.2/python.html
```

### Setup SEMAFOR
To use the SEMAFOR frame semantic parser, modify the `scripts/setup.sh` file:
```bash
# SEMAFOR options to be changed according to your env
export JAVA_HOME_BIN="/abs/path/to/java/jdk/bin"
export num_threads=2 # number of threads to use
export min_ram=4g # min RAM allocated to the JVM in GB. Corresponds to the -Xms argument
export max_ram=8g # max RAM allocated to the JVM in GB. Corresponds to the -Xmx argument

# SEMAFOR hyperparameters
export kbest=1 # keep k-best parse
export lambda=0.000001 # hyperparameter for argument identification. Refer to Kshirsagar et al. (2015) for details.
export batch_size=4000 # number of batches processed at once for argument identification.
export save_every_k_batches=400 # for argument identification
export num_models_to_save=60 # for argument identification
```

### Setup SIMPLEFRAMEID
If you intend to use SIMPLEFRAMEID for frame identification, you will need to install the following packages (on python 2.7):
```
pip install keras==2.0.6 lightfm==1.13 sklearn numpy==1.13.1 networkx==1.11 tensorflow==1.3.0
```

### Using the SEMEVAL PERL evaluation scripts

If you intend to use the SEMEVAL perl evaluation scripts, make sure
to have the `App::cpanminus` and `XML::Parser` modules installed:
```
cpan App::cpanminus
cpanm XML::Parser
```

### Using bash scripts

Each script comes with a helper: check it out with `--help`!

**Careful!** most scripts expect data output by `pyfn convert ...`
to be located under `pyfn/experiments/xp_XYZ/data` where `XYZ` stands for
the experiments number and is specified using the `-x XYZ` argument, and where
the `experiments` directory is located at the same level as the `scripts`
directory. This opinionated choice has proven extremely useful in launching
scripts by batch on a large set of experiments as it avoids having to input
the full path each time.

**Make sure to use**

```bash
pyfn convert \
  --from ... \
  --to ... \
  --source ... \
  --target /abs/path/to/pyfn/experiments/xp_XYZ/data \
  --splits ...
```

**BEFORE** calling `preprocess.sh`, `prepare.sh`, `semafor.sh` or
`open-sesame.sh`

### preprocess.sh

Use `preprocess.sh` to POS-tag and dependency-parse FrameNet splits generated
with `pyfn convert ...`. The helper should display:

```
Usage: ${0##*/} [-h] -x XP_NUM -t {mxpost,nlp4j} -p {semafor,open-sesame} [-d {mst,bmst,barch}] [-v]
Preprocess FrameNet train/dev/test splits.

  -h, --help                           display this help and exit
  -x, --xp      XP_NUM                 xp number written as 3 digits (e.g. 001)
  -t, --tagger  {mxpost,nlp4j}         pos tagger to be used: 'mxpost' or 'nlp4j'
  -p, --parser  {semafor,open-sesame}  frame semantic parser to be used: 'semafor' or 'open-sesame'
  -d, --dep     {mst,bmst,barch}       dependency parser to be used: 'mst', 'bmst' or 'barch'
  -v, --dev                            if set, script will also preprocess dev splits
```

Suppose you generated FrameNet splits for SEMAFOR using:

```bash
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_001/data \
  --splits train \
  --output_sentences
```

You can preprocess those splits with NLP4J and BMST using

```bash
./preprocess.sh -x 001 -t nlp4j -d bmst -p semafor
```

### prepare.sh

Use `prepare.sh` to automatically generate misc. data required by the
frame semantic parsing pipeline, such as gold SEMEVAL XML files for scoring,
the `framenet.frame.element.map` and the hierarchy `.csv` files
used by SEMAFOR, or the `frames.xml` and `frRelations.xml` files used by
both SEMAFOR and OPEN-SESAME. The helper should display:

```
Usage: ${0##*/} [-h] -x XP_NUM -p {semafor,open-sesame} -s {dev,test} -f FN_DATA_DIR [-u] [-e]
Prepare misc. data for frame semantic parsing.

  -h, --help                                   display this help and exit
  -x, --xp              XP_NUM                 xp number written as 3 digits (e.g. 001)
  -p, --parser          {semafor,open-sesame}  frame semantic parser to be used: 'semafor' or 'open-sesame'
  -s, --splits          {dev,test}             which splits to score: dev or test
  -f, --fn              FN_DATA_DIR            absolute path to FrameNet data directory
  -u, --with_hierarchy                         if specified, will use the hierarchy feature
  -e, --with_exemplars                         if specified, will use the exemplars
```

Suppose you generated FrameNet splits for SEMAFOR using:

```bash
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_001/data \
  --splits train \
  --output_sentences
```

You can prepare SEMAFOR data using:

```bash
./prepare.sh -x 001 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### frameid.sh

Use `frameid.sh` to perform frame identification using SIMPLEFRAMEID.
The helper should display:

```
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-p {semafor,open-sesame}]
Perform frame identification.

  -h, --help                            display this help and exit
  -m, --mode                            train on all models or decode using a single model
  -x, --xp       XP_NUM                 xp number written as 3 digits (e.g. 001)
  -p, --parser   {semafor,open-sesame}  formalize decoded frames for specified parser
```

Suppose you generated FrameNet splits for SEMAFOR using:

```bash
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_101/data \
  --splits train \
  --output_sentences
```

*After preprocessing*, you can train the SIMPLEFRAMEID parser using:

```bash
./frameid.sh -m train -x 101
```

and decode (**before decoding argument identification**) using:

```bash
./frameid.sh -m decode -x 101 -p semafor
```

### semafor.sh

Use `semafor.sh` to train the SEMAFOR parser or decode the test/dev splits.
The helper should display:

```
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-s {dev,test}] [-u]
Train or decode with the SEMAFOR parser.

  -h, --help                             display this help and exit
  -m, --mode            {train,decode}   semafor mode to use: train or decode
  -x, --xp              XP_NUM           xp number written as 3 digits (e.g. 001)
  -s, --splits          {dev,test}       which splits to use in decode mode: dev or test
  -u, --with_hierarchy                   if specified, parser will use the hierarchy feature
```

Suppose you generated FrameNet splits for SEMAFOR using:

```bash
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_001/data \
  --splits train \
  --output_sentences
```

*After preprocessing and preparation*, you can train the SEMAFOR parser using:

```bash
./semafor.sh -m train -x 001
```

and decode the test splits using:

```bash
./semafor.sh -m decode -x 001 -s test
```

### open-sesame.sh

Use `open-sesame.sh` to train the OPEN-SESMAE parser or decode the test/dev splits.
The helper should display:

```
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-s {dev,test}] [-d] [-u]
Train or decode with the OPEN-SESAME parser.

  -h, --help                              display this help and exit
  -m, --mode              {train,decode}  open-sesame mode to use: train or decode
  -x, --xp                XP_NUM          xp number written as 3 digits (e.g. 001)
  -s, --splits            {dev,test}      which splits to use in decode mode: dev or test
  -d, --with_dep_parses                   if specified, parser will use dependency parses
  -u, --with_hierarchy                    if specified, parser will use the hierarchy feature
```

Suppose you generated FrameNet splits for OPEN-SESAME using:

```bash
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_002/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

*After preprocessing and preparation*, you can train the SEMAFOR parser using:

```bash
./open-sesame.sh -m train -x 002
```

and decode the test splits using:

```bash
./open-sesame.sh -m decode -x 002 -s test
```

### score.sh

Use `score.sh` to obtain P/R/F1 scores for frame semantic parsing on
dev/test splits with the SEMEVAL scoring script, using gold of predicted frames.
The helper should display:

```
Usage: ${0##*/} [-h] -x XP_NUM -p {semafor,open-sesame} -s {dev,test} -f {gold,predicted}
Score frame semantic parsing with a modified version of the SEMEVAL scoring script.

  -h, --help                           display this help and exit
  -x, --xp      XP_NUM                 xp number written as 3 digits (e.g. 001)
  -p, --parser  {semafor,open-sesame}  frame semantic parser to be used: 'semafor' or 'open-sesame'
  -s, --splits  {dev,test}             which splits to score: dev or test
  -f, --frames  {gold,predicted}       score with gold or predicted frames
```

Note that scoring is done with an updated version of the SEMEVAL perl script,
in order to obtain more robust scores across setups. For a full account
of the modifications, refer to (Kabbach et al., 2018) and to the perl scripts
located under `lib/semeval/`.

To obtain scores for SEMAFOR using gold frames on test splits, use:

```bash
./score.sh -x XYZ -p semafor -s test -f gold
```

To obtain scores for SEMAFOR using predicted frames on test splits, use:

```bash
./score.sh -x XYZ -p semafor -s test -f predicted
```

## Replication

The `experiments` directory provides a detailed set of instructions to
replicate all results reported in (Kabbach et al., 2018) on experimental
butterfly effects in frame semantic parsing. Those instructions can be used
to compare the performances of different frame semantic parsers in various
experimental setups.


## Marshalling and Unmarshalling FrameNet XML data

`pyfn` provides a set of Python models to process FrameNet XML data.
Those can be used to help you build you own frame semantic parser.

The core of the `pyfn` models is the `AnnotationSet` corresponding to an
XML `<annotationSet>` tag. It stores various information
regarding a given set of FrameNet annotation for a given target in a given sentence.
The notable innovations are the `labelstore` and the `valenceunitstore`, which
store FrameNet labels (FE/PT/GF) in their original formats, and in custom
formats which may prove useful for frame semantic parsing.

Explore the various models under the `pyfn.models` directory of the `pyfn`
package.

### Unmarshalling FrameNet XML data

To convert a list of fulltext.xml files and/or lu.xml files to a generator
over `pyfn.AnnotationSet` objects, with no overlap between train/dev/test splits, use:

```python
import pyfn.marshalling.unmarshallers.framenet as fn_unmarshaller

if __name__ == '__main__':
  splits_dirpath = '/abs/path/to/framenet-1.x-with-dev/'
  splits = 'train'
  with_exemplars = False
  annosets_dict = fn_unmarshaller.get_annosets_dict(splits_dirpath,
                                                    splits, with_exemplars)
```
`splits_dirpath` should point at the directory containing train/dev/test
splits directories (see detailed structure [above](#use)).

`get_annosets_dict` will return a string to AnnotationSet generator dict.
It will ensure no overlap between train/dev/test splits.

Calling `get_annosets_dict` on `splits='test'` will return a dictionary
with a single `'test'` key. Calling `get_annosets_dict` on `splits='dev'`
will return a dictionary with two keys: `'dev'` and `'test'`.
Calling `get_annosets_dict` on `splits='train'` will return a dictionary
with three keys: `'train'`, `'dev'` and `'test'`.

To iterate over the list of AnnotationSet objects of each key, you can
then do:

```python
for (splits, annosets) in annosets_dict.items():
  print('Iterating over annotationsets for splits: {}'.format(splits))
  for annoset in annosets:
    print('annoset with #id = {}'.format(annoset._id))
```

Or simply, to iterate over a specific key values (such as train annosets):

```python
for annoset in annosets_dict['train']:
    print('annoset with #id = {}'.format(annoset._id))
```

Note that for performance, annosets is not a list but a generator.


### Unmarshalling OPEN-SESAME BIOS data

To convert a `.bios` file with its corresponding `.sentences` file to
a generator over `pyfn.AnnotationSet` objects, use:

```python
import pyfn.marshalling.unmarshallers.bios as bios_unmarshaller

if __name__ == '__main__':
  bios_filepath = '/abs/path/to/.bios'
  sent_filepath = '/abs/path/to/.sentences'
  annosets = bios_unmarshaller.unmarshall_annosets(bios_filepath,
                                                   sent_filepath)
  for annoset in annosets:
    print('annoset with #id = {}'.format(annoset._id))
```

**Important!** the `.bios` and `.sentences` files must have been generated
with `pyfn convert ... --to bios ...` with the `--filter overlap_fes`
parameter.

### Unmarshalling SEMAFOR CONLL data

To convert a `.frame.elements` file with its corresponding `.sentences`
file to a generator over `pyfn.AnnotationSet` objects, use:

```python
import pyfn.marshalling.unmarshallers.semafor as semafor_unmarshaller

if __name__ == '__main__':
  semafor_filepath = '/abs/path/to/.frame.elements'
  sent_filepath = '/abs/path/to/.sentences'
  annosets = semafor_unmarshaller.unmarshall_annosets(semafor_filepath,
                                                      sent_filepath)
  for annoset in annosets:
    print('annoset with #id = {}'.format(annoset._id))
```

### Unmarshalling SEMEVAL XML data

To convert a SEMEVAL `.xml` file with its corresponding `.sentences`
file to a generator over `pyfn.AnnotationSet` objects, use:

```python
import pyfn.marshalling.unmarshallers.semeval as semeval_unmarshaller

if __name__ == '__main__':
  xml_filepath = '/abs/path/to/semeval/.xml'
  annosetss = semeval_unmarshaller.unmarshall_annosets(xml_filepath)
```

By default `unmarshall_annosets` for SEMEVAL will return a generator over embedded annotationsets. To iterate over a single annotationset, use:

```python
for annosets in annosetss:
  for annoset in annosets:
    print('annoset with #id = {}'.format(annoset._id))
```

To return a 'flat' list of annosets, pass in the `flatten=True` parameter:

```python
import pyfn.marshalling.unmarshallers.semeval as semeval_unmarshaller

if __name__ == '__main__':
  xml_filepath = '/abs/path/to/semeval/.xml'
  annosets = semeval_unmarshaller.unmarshall_annosets(xml_filepath, flatten=True)
  for annoset in annosets:
    print('annoset with #id = {}'.format(annoset._id))
```

### Marshalling to OPEN-SESAME BIOS

To convert a dict of `splits` to `pyfn.AnnotationSet` objects to OPEN-SESAME-style `.bios`, refer to
`pyfn.marshalling.marshallers.bios.marshall_annosets_dict`

### Marshalling to SEMAFOR CONLL

To convert a dict of `splits` to `pyfn.AnnotationSet` objects to SEMAFOR-style `.frame.elements`, refer to
`pyfn.marshalling.marshallers.semafor.marshall_annosets_dict`

### Marshalling to SEMEVAL XML

To convert a list of `pyfn.AnnotationSet` objects to SEMEVAL-style `.xml`,
refer to `pyfn.marshalling.marshallers.semeval.marshall_annosets`

### Marshalling to .csv hierarchy

To convert a list of relations to a `.csv` file, refer to
`pyfn.marshalling.marshallers.hierarchy.marshall_relations`

## Citation

If you use `pyfn` please cite:
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


[release-image]:https://img.shields.io/github/release/akb89/pyfn.svg?style=flat-square
[release-url]:https://github.com/akb89/pyfn/releases/latest
[pypi-image]:https://img.shields.io/pypi/v/pyfn.svg?style=flat-square
[pypi-url]:https://pypi.org/project/pyfn/
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
