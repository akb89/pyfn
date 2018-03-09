# XP\#054

rofames on FN 1.7 FT with MXPOST + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 57.5 | 52.6 | 54.9 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_054/data \
  --splits train \
  --output_sentences
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
./rofames.sh -m decode -x 054 -s test
```

### Scoring
```
./score.sh -x 054 -p rofames -s test
```
