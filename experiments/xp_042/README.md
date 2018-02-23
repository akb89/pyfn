# XP\#042

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar |
| --- | --- | --- |
| 1.5 | TRUE | FALSE |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- | --- |
| FALSE | FALSE | FALSE | FALSE |

### Preprocessing and parsing
| POS tagger | Lemmatizer | Dependency parser | Frame semantic parser |
| --- | --- | --- | --- |
| MXPOST | NLP4J | MST | ROFAMES

## Generation
### Splits
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev/ \
  --target /path/to/experiments/xp_042/data/ \
  --splits train \
  --output_sentences \
  --excluded_frames=Test35 \
  --excluded_annosets=2019791
```

### Preprocessing

#### POS tagging
```
./path/to/pyfn/scripts/postag.sh --file /path/to/experiments/xp_042/data/train.sentences -t mxpost
```
