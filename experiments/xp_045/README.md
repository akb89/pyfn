# XP\#045

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | TRUE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
| FALSE | FALSE | FALSE | FALSE |

### Preprocessing
| POS tagger | Lemmatizer | Dependency parser |
| --- | --- | --- | --- |
| MXPOST | NLP4J | MST |

### Frame Semantic Parsing
| Parser | Hierarchy feature |
| --- | --- |
| ROFAMES | FALSE |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_045/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames Test35
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 045 -t mxpost -d mst -p rofames
```

### Training
```
./
```

### Decoding
```
./
```

### Scoring
```
./score.sh
```
