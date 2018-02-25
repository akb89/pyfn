# XP\#042

Replicating Das baseline used in Kshirsagar et al. (2015)
FN 1.5 preprocessing with MXPOST + MSTParser

No extra filtering is applied. Frames and Annosets are filtered following open-sesame and train/dev/test splits match open-sesame

## Score

### Test
| P| R | F1 |
| --- | --- | --- |
| 65.2 | 53.8 | 59.0 |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | FALSE | GOLD |

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
