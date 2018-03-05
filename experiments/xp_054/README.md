# XP\#054

on CLCL9

ROFAMES on FN 1.7 FT with MXPOST + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.7 | TRUE | FALSE | GOLD |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7 \
  --target /path/to/experiments/xp_054/data \
  --splits train \
  --output_sentences \
  --excluded_sentences 4106364
```

### Data preparation
```
./prepare.sh -x 054 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 054 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 054
```

### Decoding
```
./
```

### Scoring
```
./score.sh
```
