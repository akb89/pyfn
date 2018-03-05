# XP\#051

open-sesame on FN 1.5 FT with MXPOST + MST + HIERARCHY

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | FALSE | GOLD |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_051/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 051 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 051 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 051 -u
```

### Decoding
```
./rofames.sh -m decode -x 051 -s test -u
```

### Scoring
```
./score.sh -x 051 -p rofames -s test
```
