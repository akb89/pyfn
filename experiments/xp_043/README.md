# XP\#043

## Setup
| FrameNet version | Fulltext | Exemplar | POS tagger | Lemmatizer | Dependency parser | Frame semantic parser |
| --- | --- | --- | --- | --- | --- | --- |
| 1.5 | True | False | MXPOST | NLP4J | - | OPEN-SESAME

## Splits
Splits are generated with:
```
pyfn convert --from fnxml --to bios --source /path/to/fndata-1.5-with-dev --target /path/to/experiments/xp_043/data/ --splits train --output_sentences --excluded_frames=Test35 --excluded_annosets=2019791
```
