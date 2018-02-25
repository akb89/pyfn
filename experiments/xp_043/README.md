# XP\#043

## Score

### Test
| P| R | F1 |
| --- | --- | --- |
|  |  | |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | FALSE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
| FALSE | TRUE | FALSE | FALSE |

### Preprocessing
| POS tagger | Lemmatizer | Dependency parser |
| --- | --- | --- | --- |
| MXPOST | NLP4J | - |

### Frame Semantic Parsing
| Parser | Hierarchy feature |
| --- | --- |
| OPEN-SESAME | FALSE |

## Generation
### Splits
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev
  --target /path/to/experiments/xp_043/data/ \
  --splits train \
  --output_sentences \
  --excluded_frames=Test35
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 043 -t mxpost -p open-sesame
```
