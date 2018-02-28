# XP\#048

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  | |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.7 | TRUE | FALSE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
| FALSE | TRUE | FALSE | FALSE |

### Preprocessing
| POS tagger | Lemmatizer | Dependency parser |
| --- | --- | --- |
| NLP4J | NLP4J | - |

### Frame Semantic Parsing
| Parser | Hierarchy feature |
| --- | --- |
| OPEN-SESAME | FALSE |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev
  --target /path/to/experiments/xp_048/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
  --filter overlap_fes
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 048 -t nlp4j -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 048
```

### Decoding
```
./open-sesame.sh
```

### Scoring
```
./score.sh
```
