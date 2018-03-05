# XP\#052

open-sesame on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | TRUE | GOLD |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_052/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter non_breaking_spaces
```

### Data preparation
```
./prepare.sh -x 052 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 052 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 052 -u
```

### Decoding
```
./rofames.sh -m decode -x 052 -s test -u
```

### Scoring
```
./score.sh -x 052 -p rofames -s test
```
