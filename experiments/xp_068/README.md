# XP\#068

ROFAMES on FN 1.7 FT  with MXPOST + MST

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
  --target /path/to/experiments/xp_068/data \
  --splits train \
  --output_sentences \
  --excluded_sentences 4106364
```

### Data preparation
```
./prepare.sh -x 068 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 068 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 068
```

### Decoding
```
./
```

### Scoring
```
./score.sh
```
