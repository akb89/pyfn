# Replication

pyfn provides a set of models and utils to apply custom preprocessing
pipelines to FrameNet XML data and perform frame semantic parsing using
SEMAFOR, OPEN-SESAME or SIMPLEFRAMEID.

Currently supported POS taggers include:
- MXPOST
- NLP4J

Currently supported dependency parsers include:
- MST
- BIST BARCH
- BIST BMST

Currently supported frame semantic parsers include:
- SIMPLEFRAMEID for frame identification
- SEMAFOR for argument identification
- OPEN-SESAME for argument identification

## Download
Download the following:
- [data.7z](https://github.com/akb89/pyfn/releases/download/v0.1.0/data.7z) containing all the FrameNet splits for FN 1.5 and FN 1.7
- [lib.7z](https://github.com/akb89/pyfn/releases/download/v0.1.0/lib.7z) containing all the different external softwares (taggers, parsers, etc.)
- [resources.7z](https://github.com/akb89/pyfn/releases/download/v0.1.0/resources.7z) containing all the required resources
- [scripts.7z]() containing the set of bash scripts to call the different parsers and preprocessing toolkits

Extract the content of all the archives via `7z x archive_name.7z` under a
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

## Install
```
pip3 install pyfn
```

## Setup

### Using NLP4J for POS tagging
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

### Using BIST or OPEN-SESAME
If you intend to use the [BIST]() for dependency parsing or
[OPEN-SESAME]() for frame semantic parsing, you need
to install DyNET 2.0.2 following:
```
https://dynet.readthedocs.io/en/2.0.2/python.html
```

### Using SEMAFOR
To use the SEMAFOR frame semantic parser, modify the `scripts/setup.sh` file:
```bash
# SEMAFOR options to be changed according to your env
export JAVA_HOME_BIN="/Library/Java/JavaVirtualMachines/jdk1.8.0_20.jdk/Contents/Home/bin"
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

### Using the SEMEVAL PERL evaluation scripts
If you intend to use the SEMEVAL perl evaluation scripts, make sure
to have the `App::cpanminus` and `XML::Parser` modules installed:
```
cpan App::cpanminus
cpanm XML::Parser
```

## Replication
The `experiments` directory provides a detailed set of instructions to
replicate all results reported in (Kabbach et al., 2018) on experimental
butterfly effects in frame semantic parsing. Those instructions can be used
to compare the performances of different frame semantic parsers in various
experimental setups.

## Citation
If you use pyfn please cite:
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
