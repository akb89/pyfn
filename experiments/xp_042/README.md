# XP\#042

Replicating Das baseline used in Kshirsagar et al. (2015)
FN 1.5 no dev split preprocessing with MXPOST + MSTParser

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | FALSE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
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
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_042/data \
  --splits train \
  --output_sentences \
  --excluded_frames=Test35 \
  --excluded_annosets=2019791
```

### Preprocessing

```
./preprocess.sh -x 042 -t mxpost -d mst -p rofames
```

## Score

### Test
| P| R | F1 |
| --- | --- | --- |
| 65.2 | 53.8 | 59.0 |
